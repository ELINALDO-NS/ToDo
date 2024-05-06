import flet as ft
import sqlite3


class ToDo:
    def __init__(self,page:ft.page):
        self.page = page
        self.page.bgcolor = ft.colors.WHITE
        self.page.window_width = 350
        self.page.window_height = 450
        self.page.window_resizable = False
        self.page.window_always_on_top = True
        self.page.title = "ToDo App"
        self.task = ""
        self.view = "all"
        
        self.db_execute("CREATE TABLE IF NOT EXISTS TASKS(NOME,STATUS)")
        self.results = self.db_execute("SELECT * FROM TASKS")
        self.main_page()
    def db_execute(self,query,params = []):
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute(query,params)
            conn.commit()
            return cur.fetchall()




    def checked(self,e):
        is_checked = e.control.value
        label = e.control.label
        if is_checked:
            self.db_execute("UPDATE TASKS SET STATUS = 'complete' where nome = ?",params=[label])
        else:
            self.db_execute("UPDATE TASKS SET STATUS = 'incomplete' where nome = ?",params=[label])
       
        if self.view == "all":
           self.results =  self.db_execute("SELECT * FROM TASKS")
        else:
             self.results = self.db_execute("SELECT * FROM TASKS WHERE STATUS = ?",params=[self.view])
                
            
        self.update_tasks_list()

    def tasks_container(self):
        return ft.Container(
            height=self.page.height * 0.8,
            content = ft.Column(
                controls=[
                    ft.Checkbox(
                        on_change = self.checked,
                        label=res[0],
                        value=True if res[1] == "complete" else False, )
                    for res in self.results
                ]
            )
        )
    def set_value(self,e):
        self.task = e.control.value
        

    def add(self, e, imput_task):
        name = self .task
        status = "Incomplete"

        if name:
            self.db_execute("INSERT INTO TASKS VALUES(?,?)",params=[name,status])
            imput_task.value = ""
            self.results = self.db_execute("SELECT * FROM TASKS")            
            self.update_tasks_list()

    def update_tasks_list(self):
        tasks =self.tasks_container()
        self.page.controls.pop()
        self.page.add(tasks)
        self.page.update()


    def tabs_chang(self,e):
        if e.control.selected_index ==0:
            self.results = self.db_execute("SELECT * FROM TASKS")
            self.view == "all"
        elif e.control.selected_index == 1:
             self.results = self.db_execute("SELECT * FROM TASKS WHERE STATUS = 'incomplete'")
             self.view == "icomplete"
        elif e.control.selected_index ==2:
            self.results = self.db_execute("SELECT * FROM TASKS WHERE STATUS = 'complete'")
            self.view == "complete"
        self.update_tasks_list()

    def main_page(self):
       imput_task = ft.TextField(hint_text="Digite aqui uma tarefa!",expand=True, on_change=self.set_value)
       imput_bar = ft.Row(
           controls=[
               imput_task,
               ft.FloatingActionButton(
                   icon=ft.icons.ADD,
                   on_click=lambda e: self.add(e,imput_task)
                   )
           ]
       )
       tabs = ft.Tabs(
           on_change=self.tabs_chang,
           selected_index = 0,
           tabs=[
               ft.Tab(text="Todos"),
               ft.Tab(text="Em Andamento"),
               ft.Tab(text="Finalizados")           
           ]
       )
       tasks = self.tasks_container()


       self.page.add(imput_bar,tabs,tasks)

ft.app(target=ToDo)

