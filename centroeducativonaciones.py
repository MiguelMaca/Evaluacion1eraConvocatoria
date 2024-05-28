from graphviz import Digraph
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class Estudiante:
    def __init__(self, student_id, name, phone):
        self.student_id = student_id
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None

class EstudianteABB:
    def __init__(self):
        self.root = None

    def add(self, student_id, name, phone):
        new_student = Estudiante(student_id, name, phone)
        if not self.root:
            self.root = new_student
        else:
            self._add(self.root, new_student)

    def _add(self, node, new_student):
        if new_student.student_id < node.student_id:
            if node.left:
                self._add(node.left, new_student)
            else:
                node.left = new_student
        else:
            if node.right:
                self._add(node.right, new_student)
            else:
                node.right = new_student

    def search(self, student_id):
        return self._search(self.root, student_id)

    def _search(self, node, student_id):
        if not node or node.student_id == student_id:
            return node
        if student_id < node.student_id:
            return self._search(node.left, student_id)
        else:
            return self._search(node.right, student_id)

    def delete(self, student_id):
        self.root = self._delete(self.root, student_id)

    def _delete(self, node, student_id):
        if not node:
            return node
        if student_id < node.student_id:
            node.left = self._delete(node.left, student_id)
        elif student_id > node.student_id:
            node.right = self._delete(node.right, student_id)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.student_id = temp.student_id
            node.name = temp.name
            node.phone = temp.phone
            node.right = self._delete(node.right, temp.student_id)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def list_students(self):
        students = []
        self._in_order_traversal(self.root, students)
        return students

    def _in_order_traversal(self, node, students):
        if node:
            self._in_order_traversal(node.left, students)
            students.append((node.student_id, node.name, node.phone))
            self._in_order_traversal(node.right, students)

    def generate_dot(self, filename='bst'):
        dot = Digraph()
        if self.root:
            self._add_edges(dot, self.root)
        dot.render(filename, format='png', cleanup=True)

    def _add_edges(self, dot, node):
        if node.left:
            dot.edge(str(node.student_id), str(node.left.student_id))
            self._add_edges(dot, node.left)
        if node.right:
            dot.edge(str(node.student_id), str(node.right.student_id))
            self._add_edges(dot, node.right)


class EstudianteApp:
    def __init__(self, root):
        self.bst = EstudianteABB()
        self.root = root
        self.root.title("Centro Educativo Naciones")

        self.frame_add = tk.Frame(root)
        self.frame_add.pack(pady=10)

        self.label_id = tk.Label(self.frame_add, text="ID")
        self.label_id.grid(row=0, column=0)
        self.entry_id = tk.Entry(self.frame_add)
        self.entry_id.grid(row=0, column=1)

        self.label_name = tk.Label(self.frame_add, text="Nombre")
        self.label_name.grid(row=1, column=0)
        self.entry_name = tk.Entry(self.frame_add)
        self.entry_name.grid(row=1, column=1)

        self.label_phone = tk.Label(self.frame_add, text="Telefono")
        self.label_phone.grid(row=2, column=0)
        self.entry_phone = tk.Entry(self.frame_add)
        self.entry_phone.grid(row=2, column=1)

        self.button_add = tk.Button(self.frame_add, text="Agregar Estudiante", command=self.add_student)
        self.button_add.grid(row=3, columnspan=2, pady=5)

        self.frame_search = tk.Frame(root)
        self.frame_search.pack(pady=10)

        self.label_search_id = tk.Label(self.frame_search, text="Buscar ID")
        self.label_search_id.grid(row=0, column=0)
        self.entry_search_id = tk.Entry(self.frame_search)
        self.entry_search_id.grid(row=0, column=1)

        self.button_search = tk.Button(self.frame_search, text="Buscar Estudiante", command=self.search_student)
        self.button_search.grid(row=1, columnspan=2, pady=5)

        self.frame_list = tk.Frame(root)
        self.frame_list.pack(pady=10)

        self.button_list = tk.Button(self.frame_list, text="Lista de los estudiantes", command=self.list_students)
        self.button_list.pack(pady=5)

        self.listbox_students = tk.Listbox(self.frame_list, width=50)
        self.listbox_students.pack()

        self.button_visualize = tk.Button(root, text="Visualizar ABB", command=self.visualize_bst)
        self.button_visualize.pack(pady=10)

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

    def add_student(self):
        try:
            student_id = int(self.entry_id.get())
            name = self.entry_name.get()
            phone = self.entry_phone.get()
            if name and phone:
                self.bst.add(student_id, name, phone)
                messagebox.showinfo("Listo", "Estudiante Agregado!")
                self.entry_id.delete(0, tk.END)
                self.entry_name.delete(0, tk.END)
                self.entry_phone.delete(0, tk.END)
            else:
                messagebox.showwarning("Error", "Llene todos los campos")
        except ValueError:
            messagebox.showwarning("Error", "ID Invalido")

    def search_student(self):
        try:
            student_id = int(self.entry_search_id.get())
            student = self.bst.search(student_id)
            if student:
                messagebox.showinfo("Encontrado", f"ID: {student.student_id}\nNombre: {student.name}\nTelefono: {student.phone}")
            else:
                messagebox.showwarning("No encontrado", "No se encontro el estudiante")
        except ValueError:
            messagebox.showwarning("Error", "ID invalido")

    def list_students(self):
        self.listbox_students.delete(0, tk.END)
        students = self.bst.list_students()
        for student_id, name, phone in students:
            self.listbox_students.insert(tk.END, f"ID: {student_id}, Nombre: {name}, Telefono: {phone}")

    def visualize_bst(self):
        try:
            self.bst.generate_dot('ABB')
            self.display_image('ABB.png')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la imagen: {str(e)}")

    def display_image(self, filename):
        try:
            image = Image.open(filename)
            image = image.resize((800, 600), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")


root = tk.Tk()
app = EstudianteApp(root)
root.mainloop()
