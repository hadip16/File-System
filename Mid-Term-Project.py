class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None

    def path(self):
        node = self
        result = []
        while node:
            result.insert(0, node.name)
            node = node.parent
        return '/' + '/'.join(result[1:])

class File(Node):
    def __init__(self, name):
        super().__init__(name)
        self.lines = []

    def copy(self):
        new_file = File(self.name)
        new_file.lines = self.lines[:]
        return new_file

class Directory(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = {}

    def add(self, node):
        if node.name in self.children:
            print(f"Item '{node.name}' already exists")
        else:
            node.parent = self
            self.children[node.name] = node

    def remove(self, name):
        if name in self.children:
            del self.children[name]
        else:
            print("Item not found")

    def get(self, name):
        return self.children.get(name)

    def copy(self):
        new_dir = Directory(self.name)
        for child in self.children.values():
            new_dir.add(child.copy())
        return new_dir

class FileSystem:
    def __init__(self):
        self.root = Directory('/')
        self.current = self.root

    def resolve(self, path):
        node = self.root if path.startswith('/') else self.current
        parts = path.strip('/').split('/')
        for part in parts:
            if part == '..':
                node = node.parent if node.parent else node
            elif part == '.' or part == '':
                continue
            else:
                if isinstance(node, Directory):
                    node = node.get(part)
                    if not node:
                        raise ValueError("Path not found")
                else:
                    raise ValueError("Not a directory")
        return node

    def mkdir(self, name):
        self.current.add(Directory(name))

    def touch(self, name):
        self.current.add(File(name))
        print(f"File '{name}' created in the current directory.")

    def ls(self):
        for name, node in self.current.children.items():
            suffix = " folder" if isinstance(node, Directory) else ""
            print(name + suffix)

    def cd(self, path):
        try:
            node = self.resolve(path)
            if isinstance(node, Directory):
                self.current = node
            else:
                print("Not a folder")
        except Exception as e:
            print(e)

    def rm(self, name):
        self.current.remove(name)

    def rename(self, old_name, new_name):
        node = self.current.get(old_name)
        if not node:
            print("Item not found")
        elif new_name in self.current.children:
            print("New name already exists")
        else:
            del self.current.children[old_name]
            node.name = new_name
            self.current.add(node)

    def mv(self, source, dest):
        try:
            src_node = self.resolve(source)
            dst_node = self.resolve(dest)
            if isinstance(dst_node, Directory):
                src_node.parent.remove(src_node.name)
                dst_node.add(src_node)
            else:
                print("Destination is not a folder")
        except Exception as e:
            print(e)

    def cp(self, source, dest):
        try:
            src_node = self.resolve(source)
            dst_node = self.resolve(dest)
            if isinstance(dst_node, Directory):
                dst_node.add(src_node.copy())
            else:
                print("Destination is not a folder")
        except Exception as e:
            print(e)

    def cat(self, path):
        try:
            file = self.resolve(path)
            if isinstance(file, File):
                for line in file.lines:
                    print(line)
            else:
                print("Not a file")
        except Exception as e:
            print(e)

    def nwfiletxt(self, path):
        try:
            file = self.resolve(path)
            if isinstance(file, File):
                print("enter the lines (/end/ means done)")
                file.lines = []
                while True:
                    line = input()
                    if line == '/end/': break
                    file.lines.append(line)
            else:
                print("Not a file")
        except Exception:
            print("file was not found")

    def appendtxt(self, path):
        try:
            file = self.resolve(path)
            if isinstance(file, File):
                print("enter the lines (/end/ means done)")
                while True:
                    line = input()
                    if line == '/end/': break
                    file.lines.append(line)
            else:
                print("file was not found")
        except Exception:
            print("file was not found")

    def run(self):
        while True:
            try:
                command = input(self.current.path() + "$ ").strip()
                if not command:
                    continue
                parts = command.split()
                cmd, args = parts[0], parts[1:]

                if cmd == 'exit': break
                elif cmd == 'mkdir' and args: self.mkdir(args[0])
                elif cmd == 'touch' and args: self.touch(args[0])
                elif cmd == 'ls': self.ls()
                elif cmd == 'cd' and args: self.cd(args[0])
                elif cmd == 'rm' and args: self.rm(args[0])
                elif cmd == 'rename' and len(args) == 2: self.rename(args[0], args[1])
                elif cmd == 'mv' and len(args) == 2: self.mv(args[0], args[1])
                elif cmd == 'cp' and len(args) == 2: self.cp(args[0], args[1])
                elif cmd == 'cat' and args: self.cat(args[0])
                elif cmd == 'nwfiletxt' and args: self.nwfiletxt(args[0])
                elif cmd == 'appendtxt' and args: self.appendtxt(args[0])
                else:
                    print("Unknown command arguments")
            except Exception as e:
                print("Error:", e)

if __name__ == '__main__':
    fs = FileSystem()
    fs.run()
