def TrubText(Trub:str = None,text:str = None,guid:str = None):
	if Trub == "MentionText":
		if guid and text != None:
			return [{"type":"MentionText","mention_text_object_guid":guid,"from_index":0,"length":len(text),"mention_text_object_type":"User"}]
	if Trub == "Mono":
		if text != None:
			return [{"from_index": 0, "length": len(text), "type": "Mono"}]
	elif Trub == "Bold":
		if text != None:
			return [{"from_index": 0, "length": len(text), "type": "Bold"}]
	elif Trub == "Italic":
		if text != None:
			return [{"from_index": 0, "length": len(text), "type": "Italic"}]

