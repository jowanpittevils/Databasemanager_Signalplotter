import pickle
f = open("test.pkl","rb")
test = pickle.load(f)
print(len(test))