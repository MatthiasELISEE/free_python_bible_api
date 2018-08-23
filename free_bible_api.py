import xmltodict
import re
from collections import OrderedDict

bible = "!failed"

def set_bible(file_name):
	global bible
	try:
		with open(file_name) as fd:
			bible = xmltodict.parse(fd.read())
			bible = bible['osis']['osisText']['div']
	except KeyError:
		raise Exception('Your xml OSIS bible is not correctly formatted.')		

# only works for french and english without accents
def osisID_from_reference(reference):
	reference = reference.replace(" ","").lower()
	print(reference)
	parts = re.search("(\d?[a-z]+)(\d+)[:,.](\d+)",reference)
	book = parts.group(1)
	osis_chapter = parts.group(2)
	osis_verse = parts.group(3)
	
	#Esther not at the right place, but is just before Ezra
	#James not at the right place, but is just after Luke
	
	if "gen" in book:
		osis_book="Gen"
	elif "exo" in book:
		osis_book="Exod"
	elif "lev" in book:
		osis_book="Lev"
	elif "deut" in book:
		osis_book="Num"
	elif "jos" in book:
		osis_book="Josh"
	elif "jug" in book or "judg" in book:
		osis_book="Judg"
	elif "ruth" in book:
		osis_book="Ruth"
	elif "1s" in book:
		osis_book="1Sam"
	elif "2s" in book:
		osis_book="2Sam"
	elif "1k" in book or "1r" in book:
		osis_book="1Kgs"
	elif "2k" in book or "2r" in book:
		osis_book="2Kgs"
	elif "1ch" in book:
		osis_book="1Chr"
	elif "2ch" in book:
		osis_book="2Chr"
	elif book.startswith('est'): 
		osis_book="Esth"
	elif book.startswith('e'):
		osis_book="Ezra"
	elif book.startswith('n'):
		osis_book="Neh"
	elif "job" in book:
		osis_book="Job"
	elif book.startswith("ps"):
		osis_book="Ps"
	elif book.startswith("pr"):
		osis_book="Prov"
	elif "ecc" in book:
		osis_book="Eccl"
	elif "song" in book or "cant" in book:
		osis_book="Song"
	elif "isa" in book or "esa" in book:
		osis_book="Isa"
	elif "jer" in book:
		osis_book="Jer"
	elif "lam" in book:
		osis_book="Lam"
	elif "eze" in book:
		osis_book="Ezek"
	elif "dan" in book:
		osis_book="Dan"
	elif book.startswith("ho") or book.startswith ("os"):
		osis_book="Hos"
	elif book.startswith("jo"):
		osis_book="Joel"
	elif book.startswith("am"):
		osis_book="Amos"
	elif book.startswith("ob"):
		osis_book="Obad"
	elif book.startswith("mi"):
		osis_book="Mic"
	elif "nah" in book:
		osis_book="Nah"
	elif "hab" in book:
		osis_book="Hab"
	elif "ph" in book and not book.startswith('ph'):
		osis_book="Zeph"
	elif book.startswith('agg') or book.startswith('hag'):
		osis_book="Hag"
	elif book.startswith("z"):
		osis_book="Zech"
	elif book.startswith("ma"):
		osis_book='Mal'
		
	elif book.startswith("mt") or book.startswith("mat"):
		osis_book="Matt"
	elif book.startswith("ma"):
		osis_book="Mark"
	elif book.startswith("lu"):
		osis_book="Luke"
	elif book.startswith("ja"):
		osis_book="Jas"
	elif book.startswith("j"):
		osis_book="John"
	elif book.startswith("a"):
		osis_book="Acts"
	elif book.startswith("ro") or book.startswith("rm"):
		osis_book="Rom"
	elif book.startswith("1c"):
		osis_book="1Cor"
	elif book.startswith("2c"):
		osis_book="2Cor"
	elif book.startswith("g"):
		osis_book="Gal"
	elif book.startswith("e"):
		osis_book="Eph"
	elif "pp" in book:
		osis_book="Phil"
	elif book.startswith("c"):
		osis_book="Col"
	elif book.startswith("1th"):
		osis_book="1Thess"
	elif book.startswith("2th"):
		osis_book="2Thess"
	elif "1t" in book:
		osis_book="1Tim"
	elif "2t" in book:
		osis_book="2Tim"
	elif book.startswith("t"):
		osis_book="Titus"
	elif book.startswith("p"):
		osis_book="Phlm"
	elif book.startswith("h"):
		osis_book="Heb"
	elif book.startswith("1p"):
		osis_book="1Pet"
	elif book.startswith("2p"):
		osis_book="2Pet"
	elif book.startswith("1"):
		osis_book="1John"
	elif book.startswith("2"):
		osis_book="2John"
	elif book.startswith("3"):
		osis_book="3John"
	elif book.startswith("j"):
		osis_book="Jude"
	elif book.startswith("r"):
		osis_book="Rev"
		
	return osis_book+"."+osis_chapter+"."+osis_verse

def text_from_osisID(osisID):
	global bible
	if bible=="!failed":
		raise IOError('You forgot to set the bible using the set_bible function. Sorry.')
	book_trigger = False
	chapter_trigger = False
	verse_trigger = False
	
	returned = ""
	
	for book in bible:
		if book['@osisID'] == osisID:
			book_trigger = True
		
		# Workaround for 1-chapter books
		if type(book['chapter'])==OrderedDict:
			chapters = [book['chapter']]
		else:
			chapters = book['chapter']
		
		for chapter in chapters:
			# Workaround to solve the problem of the preceding workaround
			if type(chapter) != OrderedDict:
				chapter = chapter[0]
				
			if chapter['@osisID'] == osisID:
				chapter_trigger = True
				
			
			# But there's no 1-verse chapter lmbo
			for verse in chapter['verse']:
				if verse['@osisID'] == osisID:
					verse_trigger = True
				
				if verse_trigger or chapter_trigger or book_trigger:
					returned += verse['#text'] + "\n"
				
				verse_trigger = False
			chapter_trigger = False
		book_trigger = False
	
	if returned=="":
		return "!failed"
	return returned

def text_from_reference(reference):
	return reference+" : "+text_from_osisID(osisID_from_reference(reference))

def text_from_references(reference):
	reference_list = reference.split(';')
	osisID_list = [osisID_from_reference(r) for r in reference_list]
	splitted_references=[]
	
	for r in reference_list:
		rs = r.split("-")
		if len(rs)<2:
			continue
		elif len(rs)>2:
			raise IOError("There are too much '-'")
		else:
			end = int(float(rs[1]))
			osisID_start = osisID_from_reference(rs[0])
			osisID = osisID_start.split(".")
			start = int(float(osisID[2]))
			del osisID[2]
			for i in range(start, end+1):
				splitted_references.append(''.join([osisID[0]]+[" "]+[osisID[1]]+[":"]+[str(i)]))
		reference_list.remove(r)
	
	reference_list=splitted_references+reference_list
	return ''.join(text_from_reference(str(s)) for s in reference_list)
set_bible("lsg.xml")
print(text_from_references("Amo 3:4-6; jude 4,6; Gen7.8"))
# using it with node https://ourcodeworld.com/articles/read/286/how-to-execute-a-python-script-and-retrieve-output-data-and-errors-in-node-js