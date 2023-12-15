from flask import Flask, render_template, request
from pymongo import MongoClient
import math
import re

client=MongoClient()
client=MongoClient('mongodb://localhost:27017/')

db=client['sample']

app = Flask(__name__)
app.secret_key = 'password'
users=db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        firstname = request.form['Firstname']
        lastname = request.form['Lastname']
        username = request.form['email']
        password = request.form['password']
        hist1=[]
        hist2=[]

        if db.users.find_one({'username': username}):
            return "Username already exists"
        
        user_data = {'username': username, 'password': password,
                     'firstname': firstname, 'lastname': lastname,
                     'history1':hist1, 'history2':hist2}
        db.users.insert_one(user_data)

        #session['username'] = username
        
        return success()
    return render_template('signup.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        user = db.users.find_one(
            {'username': username, 'password': password})
        if user:
            
            #session['username'] = user['username']
            return success()
        else:
            return "Invalid username or password"

    return render_template('signin.html')

@app.route('/success')
def success():


    return render_template('success.html')
@app.route('/mainn')
def mainn():
    return render_template('mainn.html')

@app.route('/mainn', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected"
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected"

    file.save('check1.txt')

    if 'sec' not in request.files:
        return "No file selected"
    
    file1 = request.files['sec']
    if file1.filename == '':
        return "No file selected"

    file1.save('check2.txt')

    def rephrase(phrase):
        return re.sub(r"(\s+|[@$&*%#:;',!]*)","",phrase.lower())
    
    class Node:
        def __init__(self, order):
            self.order = order
            self.values = []
            self.keys = []
            self.nextKey = None
            self.parent = None
            self.check_leaf = False

    class Bplustree():
        def __init__(self, order,length):
            self.order = order
            self.length = length
            self.root = None
            self.con=[]
            self.ans=[]
            self.f_w=""
            self.s=''
            self.li=[",","_","."]
        def ins(self, value, key):
            value = str(value)
            old_node = self.search(value)
            old_node.insert_at_leaf(old_node, value, key)

            if (len(old_node.values) == old_node.order):
                node1 = Node(old_node.order)
                node1.check_leaf = True
                node1.parent = old_node.parent
                mid = int(math.ceil(old_node.order / 2)) - 1
                node1.values = old_node.values[mid + 1:]
                node1.keys = old_node.keys[mid + 1:]
                node1.nextKey = old_node.nextKey
                old_node.values = old_node.values[:mid + 1]
                old_node.keys = old_node.keys[:mid + 1]
                old_node.nextKey = node1
                self.insert_in_parent(old_node, node1.values[0], node1)

        def srch(self, value):
            current_node = self.root
            while(current_node.check_leaf == False):
                temp2 = current_node.values
                for i in range(len(temp2)):
                    if (value == temp2[i]):
                        current_node = current_node.keys[i + 1]
                        break
                    elif (value < temp2[i]):
                        current_node = current_node.keys[i]
                        break
                    elif (i + 1 == len(current_node.values)):
                        current_node = current_node.keys[i + 1]
                        break
            return current_node

        def find(self, value, key):
            l = self.search(value)
            for i, item in enumerate(l.values):
                if item == value:
                    if key in l.keys[i]:
                        return True
                    else:
                        return False
            return False

        def insert_in_parent(self, n, value, ndash):
            if (self.root == n):
                rootNode = Node(n.order)
                rootNode.values = [value]
                rootNode.keys = [n, ndash]
                self.root = rootNode
                n.parent = rootNode
                ndash.parent = rootNode
                return

            parentNode = n.parent
            temp3 = parentNode.keys
            for i in range(len(temp3)):
                if (temp3[i] == n):
                    parentNode.values = parentNode.values[:i] + \
                        [value] + parentNode.values[i:]
                    parentNode.keys = parentNode.keys[:i +
                                                    1] + [ndash] + parentNode.keys[i + 1:]
                    if (len(parentNode.keys) > parentNode.order):
                        parentdash = Node(parentNode.order)
                        parentdash.parent = parentNode.parent
                        mid = int(math.ceil(parentNode.order / 2)) - 1
                        parentdash.values = parentNode.values[mid + 1:]
                        parentdash.keys = parentNode.keys[mid + 1:]
                        value_ = parentNode.values[mid]
                        if (mid == 0):
                            parentNode.values = parentNode.values[:mid + 1]
                        else:
                            parentNode.values = parentNode.values[:mid]
                        parentNode.keys = parentNode.keys[:mid + 1]
                        for j in parentNode.keys:
                            j.parent = parentNode
                        for j in parentdash.keys:
                            j.parent = parentdash
                        self.insert_in_parent(parentNode, value_, parentdash)
        def insert(self):
            with open ("check1.txt","r") as f:
                self.f_w= (f.read ())
            for i in self.f_w:
                self.s+=i
                if i in self.li:
                    p=rephrase(self.s)
                    self.con.append(p)
                    self.s=''
            #print(self.con)
        def search(self,given):
            if (given in self.con):
                return True
            else:
                return False
        def printtree(self):
            return self.con
        def sec_part(self):
            with open ("check2.txt","r") as f:
                self.f_w= (f.read ())
            for i in self.f_w:
                self.s+=i
                if i in self.li:
                    p=rephrase(self.s)
                    self.ans.append (p)
                    self.s=''
            #print(self.ans)
        def li_to_b(self):
            match=0
            for i in self.ans:
                #print(i)
                if self.search(i):
                    match+=1
            ann= (match/len(self.ans))*100
            return ann
        def b_to_li(self):
            match=0
            for i in self.con:
                #print(i)
                if i in self.ans:
                    match+=1
            return (match/len(self.con))*100


    bplustree = Bplustree("file",10)
    bplustree.insert()
    bplustree.sec_part()
    sol1=bplustree.li_to_b()
    sol2=bplustree.b_to_li()


    return f"ans for li to b {sol1} ans for b to li {sol2}"

if __name__ == '__main__':
    app.run(debug=True)
