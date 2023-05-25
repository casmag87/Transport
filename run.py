import xml.etree.ElementTree as ET
import psycopg2

class Node:
    def __init__(self, data, column_type):
        self.left = None
        self.right = None
        self.data = data
        self.column_type = column_type

class BST:
    def __init__(self):
        self.root = None

    def insert(self, data, column_type):
        if self.root is None:
            self.root = Node(data, column_type)
        else:
            self._insert(data, column_type, self.root)

    def _insert(self, data, column_type, curr_node):
        if data < curr_node.data:
            if curr_node.left is None:
                curr_node.left = Node(data, column_type)
            else:
                self._insert(data, column_type, curr_node.left)
        elif data > curr_node.data:
            if curr_node.right is None:
                curr_node.right = Node(data, column_type)
            else:
                self._insert(data, column_type, curr_node.right)
        else:
            print("Value already present in tree.")

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, curr_node):
        if curr_node is not None:
            self._print_tree(curr_node.left)
            print(str(curr_node.data))
            self._print_tree(curr_node.right)

# Load the XML file
tree = ET.parse('4a.xml')

# Get the root element
root = tree.getroot()

# Create a binary search tree to store the data
bst = BST()

# Traverse the XML tree to find grandchildren elements and add their tag names to the binary search tree
column_types = {}
for elem in root.iter():
    if len(list(elem)) == 0: # Check if the element has no children
        column_name = elem.tag.replace("{http://www.netex.org.uk/netex}", "")
        if column_name != "ShortName":
            value = elem.text.strip() if elem.text else None
            if value is not None:
                try:
                    float_value = float(value)
                    column_types[column_name] = "DOUBLE PRECISION"
                    bst.insert(column_name, column_types[column_name])
                except ValueError:
                    if value.lower() in ["true", "false"]:
                        column_types[column_name] = "BOOLEAN"
                        bst.insert(column_name, column_types[column_name])
                    else:
                        column_types[column_name] = "TEXT"
                        bst.insert(column_name, column_types[column_name])

# Connect to PostgreSQL
with psycopg2.connect(database="Maxville", user="postgres", password="070487", host="localhost", port="5432") as conn:
    with conn.cursor() as cur:
        # Create a table if it doesn't exist
        cur.execute("CREATE TABLE IF NOT EXISTS mytable (id SERIAL PRIMARY KEY)")

        for column_name, column_type in column_types.items():
            print(column_name, column_type)
            
            cur.execute("ALTER TABLE mytable ADD COLUMN \"{}\" {}".format(column_name.lower(), column_type))

       
        
        conn.commit()