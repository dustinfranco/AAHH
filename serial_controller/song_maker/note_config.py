offs = 48
note_config = {
"E0" : 0,
"A0" : 1,
"D0" : 2,
"G0" : 3,
"B0" : 4,
"e0" : 5,
"E1" : 6,
"A1" : 7,
"D1" : 8,
"G1" : 9,
"B1" : 10,
"e1" : 11,
"E2" : 12,
"A2" : 13,
"D2" : 14,
"G2" : 15,
"B2" : 16,
"e2" : 17,
"E3" : 18,
"A3" : 19,
"D3" : 20,
"G3" : 21,
"B3" : 22,
"e3" : 23,
"E4" : 24,
"A4" : 25,
"D4" : 26,
"G4" : 27,
"B4" : 28,
"e4" : 29
}

for note in note_config:
  note_config[note] = chr(note_config[note] + offs)

