POSSIBLE_PERMISSION_LEVELS = ( 'signature|System', 'system', 'development', 'normal', 'dangerous', 'signature' )
PERMISSION_MAP_FILE = "/home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/appWindow/PERMISSION_LEVELS.txt"

'''
	Input: Location of Manifest XML file
	Output: dict with format:
			{
				'signature|System' = ['android.permission.xxx', 'android.permission.yy', ....],
				'system' = ['', '', ...],
				.....
			}
'''
def parseTxt(input_file_location):
	PERM_INDEX = {}
	with open(PERMISSION_MAP_FILE) as ff:
		for line in ff:
			tupl = line.split(" ")
			PERM_INDEX[tupl[0]] = (tupl[1])[:-1]


	permissions_dict = {}
	for p in POSSIBLE_PERMISSION_LEVELS:
		permissions_dict[p] = []

	print 'hi\n'
	print PERM_INDEX

	with open(input_file_location) as f:
		for line in f:
			line = line.strip()
			if line.find("uses-permission") != -1:
					pos = line.find("android:name") + len('android:name') + 2
					perm = line[pos : ]
					perm = perm[ : perm.find('"')]
					print perm
					if PERM_INDEX.get(perm, None) != None:
						if PERM_INDEX[perm] in permissions_dict:
							permissions_dict[PERM_INDEX[perm]].append(perm)	
			else:
				if line.find("permission") != -1 and line.find("protectionLevel") != -1:
					pos = line.find("android:protectionLevel") + len('android:protectionLevel') + 2
					prot = line[pos : ]
					prot = prot[ : prot.find('"')]
					pos = line.find("android:name") + len('android:name') + 2
					name = line[pos : ]
					name = name[ : name.find('"')]
					print prot
					if prot in permissions_dict:
						permissions_dict[prot].append(name)

			
		return permissions_dict
