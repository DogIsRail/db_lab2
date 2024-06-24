class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.values = [] if is_leaf else None


class BPlusTree:
    def __init__(self, t):
        self.root = BPlusTreeNode(is_leaf=True)
        self.t = t

    def insert(self, name, phone):
        key = self.alphabetic_hash(name)
        root = self.root
        if len(root.keys) == 2 * self.t:
            temp = BPlusTreeNode()
            self.root = temp
            temp.children.append(root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, key, phone)
        else:
            self._insert_non_full(root, key, phone)

    def _split_child(self, parent, i):
        t = self.t
        y = parent.children[i]
        z = BPlusTreeNode(is_leaf=y.is_leaf)

        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t])

        z.keys = y.keys[t:]
        y.keys = y.keys[:t]

        if y.is_leaf:
            z.values = y.values[t:]
            y.values = y.values[:t]
        else:
            z.children = y.children[t:]
            y.children = y.children[:t + 1]

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            idx = self._find_index(node.keys, key)
            if idx < len(node.keys) and node.keys[idx] == key:
                if node.values[idx] != value:
                    node.values[idx] = value
                else:
                    print("Key already exists with the same value, skipping insertion:", key, value)
            else:
                node.keys.insert(idx, key)
                node.values.insert(idx, value)
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _find_index(self, keys, key):
        for i, k in enumerate(keys):
            if key < k:
                return i
        return len(keys)

    def search(self, name):
        key = self.alphabetic_hash(name)
        return self._search(self.root, key)

    def _search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if node.is_leaf:
            if i < len(node.keys) and key == node.keys[i]:
                return node.values[i]
            else:
                return None
        elif i < len(node.keys) and key == node.keys[i]:
            return self._search(node.children[i + 1], key)
        else:
            return self._search(node.children[i], key)

    def _search_node(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if node.is_leaf:
            if i < len(node.keys) and key == node.keys[i]:
                return node
            else:
                return None
        elif i < len(node.keys) and key == node.keys[i]:
            return self._search_node(node.children[i + 1], key)
        else:
            return self._search_node(node.children[i], key)

    def display(self, node=None, level=0):
        if node is None:
            node = self.root
        if node.is_leaf:
            print("Level", level, "Leaf:", [(key, value) for key, value in zip(node.keys, node.values)])
        else:
            print("Level", level, ":", node.keys)
            for child in node.children:
                self.display(child, level + 1)

    def alphabetic_hash(self, name):
        if type(name) == int:
            return name

        letter_encoding = {
            'а': 1, 'б': 2, 'в': 3, 'г': 4, 'ґ': 5, 'д': 6, 'е': 7, 'є': 8, 'ж': 9, 'з': 10,
            'и': 11, 'і': 12, 'ї': 13, 'й': 14, 'к': 15, 'л': 16, 'м': 17, 'н': 18, 'о': 19, 'п': 20,
            'р': 21, 'с': 22, 'т': 23, 'у': 24, 'ф': 25, 'х': 26, 'ц': 27, 'ч': 28, 'ш': 29, 'щ': 30,
            'ь': 31, 'ю': 32, 'я': 33,
        }
        name = name.lower()
        hash_value = ''
        for c in name[:5]:
            n = str(letter_encoding[c])
            if len(n) == 1:
                n = '0' + n
            hash_value += n
        return int(hash_value)

    def delete(self, name):
        key = self.alphabetic_hash(name)
        node = self._search_node(self.root, key)
        i = node.keys.index(key)
        node.keys.pop(i)
        node.values.pop(i)

        if len(node.keys) < 2:
            keys, values = node.keys[::], node.values[::]
            del node
            for key, value in zip(keys, values):
                self.insert(key, value)

    def search_phones_greater_than(self, value):
        greater_phones = []
        for key, phone in self.retrieve_all():
            if key > value:
                greater_phones.append(phone)
        return greater_phones

    def search_phones_less_than(self, value):
        less_phones = []
        for key, phone in self.retrieve_all():
            if key < value:
                less_phones.append(phone)
        return less_phones

    def retrieve_all(self):
        all_phones = []
        self._retrieve_all(self.root, all_phones)
        return all_phones

    def _retrieve_all(self, node, all_phones):
        if node:
            if node.is_leaf:
                for i in range(len(node.keys)):
                    all_phones.append((node.keys[i], node.values[i]))
            else:
                for i in range(len(node.children)):
                    self._retrieve_all(node.children[i], all_phones)


bpt = BPlusTree(t=2)
names = ['Долженко', 'Русецька', 'Носковський', 'Лаба', 'Шморгун', 'Юхименко', 'Якутович', 'Крупська', 'Стаднюк',
         'Роговий', 'Візерські', 'Журавленко', 'Арсенюк', 'Самойлович', 'Андрющенко', 'Лозинська', 'Оробко', 'Кузьмінський']
phones = ['+380976435340', '+380682345678', '+380503456789', '+380504567890', '+380505678901', '+380506789012',
          '+380507890123', '+380508901234', '+380509012345', '+380631123456', '+380632234567', '+380633345678',
          '+380634456789', '+380635567890', '+380636678901', '+380637789012', '+380638890123', '+380639901234']

for name, phone in zip(names, phones):
    bpt.insert(name, phone)


bpt.display()


bpt.delete('Лаба')

print()
print(bpt.search("Шморгун"))
print(bpt.search("Якутович"))
print(bpt.search("Візерські"))
print(bpt.search("Самойлович"))
print()


greater_than_phones = bpt.search_phones_greater_than(bpt.alphabetic_hash('Арсенюк'))
print("Contacts with hash-function greater than 'Арсенюк':", greater_than_phones)


less_than_phones = bpt.search_phones_less_than(bpt.alphabetic_hash('Андрющенко'))
print("Contacts with hash-function less than 'Андрющенко':", less_than_phones)
