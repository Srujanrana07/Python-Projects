from tkinter import *

r = Tk()
r.title('To-Do List')
r.attributes('-alpha', 0.9)

def add_task():
    def add_task_final():
        task = inp.get()
        lb.insert(END, task)
        win.destroy()

    win = Tk()
    inp = Entry(win, font=("Arial", 25), width=20, bg='light blue', fg='black')
    inp.pack()
    confirm = Button(win, text='Add', font=("Arial", 25), width=20, height=2, bg='light blue', fg='black', command=add_task_final)
    confirm.pack()
    confirm_not = Button(win, text='Cancel', font=("Arial", 25), width=20, height=2, bg='light blue', fg='black', command=win.destroy)
    confirm_not.pack()

def delete_task():
    lb.delete(ANCHOR)

add_task_button = Button(r, text='Add Task', font=("Arial", 25), width=20, height=2, bg='light blue', fg='black',command=add_task)
add_task_button.grid(row=0, column=0, padx=50, pady=50)

delete_task_button = Button(r, text='Delete Task', font=("Arial", 25), width=20, height=2, bg='light blue', fg='black',command=delete_task)
delete_task_button.grid(row=0, column=1, padx=50, pady=50)

lb = Listbox(r, font=("Arial", 25), width=60, height=20, bg='light blue', fg='black')
lb.grid(row=1, column=0, columnspan=2, padx=50, pady=50)

r.mainloop()






# # Load emoji image
# emoji_image = pygame.image.load('emoji.png')

# # Scale emoji image to desired size
# emoji_image = pygame.transform.scale(emoji_image, (50, 50))

# # Blit emoji image to screen
# screen.blit(emoji_image, (x, y))  # Replace x and y with desired coordinates