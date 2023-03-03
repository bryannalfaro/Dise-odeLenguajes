alfabeto = ['a', 'b']
a={14: {'b': [14, 15, 17, 16],
        'a': [14, 15, 17, 16]
        },
    15: {'b': [14, 15, 17, 16],
         'a': [14, 15, 17, 16]
         },
    17: {'b': [18],
         'a': [14, 15, 17, 16]
         },
    16: {'b': [14, 15, 17, 16],
        'a': [20]
        }
    }

flipped = {}
ignored = []
for i in range(0, len(alfabeto)):
    #agrupar por esa letra
    flipped = {}
    for key, value in a.items():
        if key not in ignored:
            if alfabeto[i] in value:
                print('je',value,value[alfabeto[i]])
                if tuple(value[alfabeto[i]]) not in flipped:
                    if len(flipped)==0:
                        flipped[tuple(value[alfabeto[i]])] = [key]
                    else:
                        flipped[tuple(value[alfabeto[i]])] = [key]
                        ignored.append(key)

                else:
                    flipped[tuple(value[alfabeto[i]])].append(key)
    print("internal",flipped)


print('FLIPPEEEED',flipped,ignored)