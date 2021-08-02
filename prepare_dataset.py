
context = []

n = 7

for i in range(n, len(conversation)):
    
    row = []
    prev = i - 1 - n

    for j in range(i, prev, -1):
        row.append(conversation[j])
    context.append(i)


columns = ['response', 'context']

columns = columns + ['context/' + str(i) for i in range(n - 1)]

df = pd.DataFrame.from_records(contexted, columns=columns)

X_train, X_test, y_train, y_test = train_test_split(df.context, df.response, test_size=0.1, random_state=42)