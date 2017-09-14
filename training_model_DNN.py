import tflearn
import numpy as np

data = np.loadtxt("D:/Docs/Audio/Movies/Autograph/save25_data.txt",dtype=int)
label = np.loadtxt("D:/Docs/Audio/Movies/Autograph/save25_label.txt",dtype=int)
word_lexicon = np.genfromtxt("D:/Docs/Audio/Movies/Autograph/save25_lexicon.txt", dtype=str)
print('data shape', np.shape(data))
net = tflearn.input_data([None, np.shape(data)[1]])
net = tflearn.fully_connected(net, len(word_lexicon), activation='softmax')
net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')

# model = tflearn.DNN(net, checkpoint_path='tflearn.dnn.ckpt')
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
print('model fitting in progress...')
model.fit(data, label, n_epoch=10, batch_size=20, show_metric=True)
model.save("tflearn_dnn.tfl")

print('testing model...')
test = np.loadtxt("D:/Docs/Audio/Movies/Autograph/test_data.txt",dtype=int)
label = np.loadtxt("D:/Docs/Audio/Movies/Autograph/test_label.txt",dtype=int)

pred = model.predict(test)
print(pred)