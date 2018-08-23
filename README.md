# free_python_bible_api

You need an OSIS xml bible to proceed.

You can find them here : https://github.com/bzerangue/osis-bibles

Before getting verses you need to set the Bible file.

```python
import free_bible_api

free_bible_api.set_bible("kjv.xml")
```

There are 2 different ways to get verses :

```python

# Get verses from reference in French or English (they must be separated by semi-colons)
print(free_bible_api.text_from_references("Am 3:4-6; jude 4,6; Gen7.8"))
# The Bible can be in whatever language you want, but the reference must be in French or English.

# Get verse from OSIS id :
print(free_bible_api.text_from_osisID("Gen.5.4"))
```
You can also just translate a reference in French or English to an clean OSIS id.

```python
# Reference to OSIS ID translator
print(free_bible_api.osisID_from_reference("Genesis  5: 4"))
# prints : 
# Gen.5.4
```

Use it as much as you want, and please report bugs.

_1 Corinthians 10:31 Whether therefore ye eat, or drink, or whatsoever ye do, do all to the glory of God._
