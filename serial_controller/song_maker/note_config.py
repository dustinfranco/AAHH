offs = 48
note_config = {
"E0" : 33,
"A0" : 34,
"D0" : 35,
"G0" : 36,
"B0" : 37,
"e0" : 38,
"E1" : 31,
"A1" : 26,
"D1" : 27,
"G1" : 28,
"B1" : 29,
"e1" : 30,
"E2" : 17,
"A2" : 18,
"D2" : 19,
"G2" : 20,
"B2" : 21,
"e2" : 22,
"E3" : 9,
"A3" : 10,
"D3" : 11,
"G3" : 12,
"B3" : 15,
"e3" : 14,
"E4" : 1,
"A4" : 2,
"D4" : 3,
"G4" : 4,
"B4" : 5,
"e4" : 6
}

for note in note_config:
  note_config[note] = chr(note_config[note] + offs)

