<template>
  <q-page class="bg-grey-3 column">
    <div class="row q-pa-md bg-primary">
      <q-input
        v-model="newTask"
        @keyup.enter="addTask"
        class="col"
        square
        filled
        bg-color="white"
        placeholder="Add task"
        dense>
        <template v-slot:append>
          <q-btn @click="addTask" round dense flat icon="add" />
        </template>
      </q-input>
    </div>
    <q-list class="bg-white" separator bordered>
      <q-item
        v-for="(task, index) in this.tasks"
        :key="task.id"
        @click="updateStateToDB(task, index)"
        :class="{ 'done bg-blue-1': task.done }"
        clickable
        v-ripple>
        <!-- Checkbox section -->
        <q-item-section avatar>
          <q-checkbox v-model="task.done" class="no-pointer-events" color="primary" />
        </q-item-section>

        <!-- Task name section -->
        <q-item-section class="limit-width">
          <q-item-label lines="3">{{ task.title }}</q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-item-label v-if="task.updatedAt">
            Updated At: {{ dateFormat(task.updatedAt) }}
          </q-item-label>
          <q-item-label v-else>
            Created At: {{ dateFormat(task.createdAt) }}
          </q-item-label>
        </q-item-section>

        <!-- Update button -->
        <q-item-section side v-if="!task.done">
          <q-btn
            @click.stop="updateTask(index)"
            flat
            round
            dense
            color="primary"
            icon="update" />
        </q-item-section>

        <!-- Delete button -->
        <q-item-section side>
          <q-btn
            @click.stop="deleteTask(index)"
            flat
            round
            dense
            color="primary"
            icon="delete" />
        </q-item-section>
      </q-item>
    </q-list>
    <div v-if="!tasks.length" class="no-tasks absolute-center">
      <q-icon name="check" size="100px" color="primary" />
      <div class="text-h5 text-primary text-center">
        No tasks
      </div>
    </div>
    <div class="row justify-center q-mt-auto q-mb-md">
      <q-pagination
        v-model="currentPage"
        :max="paginationLength"
        @update:model-value="getAllTasks(currentPage, pageSize)" />
    </div>
  </q-page>
</template>

<script>
import { date } from 'quasar'
import { api } from 'src/boot/axios'
import { defineComponent, ref } from 'vue'


export default defineComponent({
  data() {
    return {
      newTask: '',
      tasks: [],
      total: 0,
      currentPage: 1,
      pageSize: 10
    }
  },
  mounted() {
    this.getAllTasks(this.currentPage, this.pageSize)
  },
  computed: {
    paginationLength() {
      let pages = Math.floor(this.total / this.pageSize)
      if (this.total % this.pageSize != 0) {
        pages++
      }
      return pages
    },
  },
  methods: {
    dateFormat(timeStamp) {
      return date.formatDate(timeStamp, 'YYYY MMMM DD, hh:mm:ss')
    },
    changeState(task) {
      return task.done = !task.done
    },
    updateStateToDB(task, index) {
      // let state = task.done = !task.done
      let state = changeState(task)
      let completion = {
        title: this.tasks[index].title,
        done: state
      }
      let task_id = this.tasks[index].id
      const response = api.put(`/todos/${task_id}`, completion)
      completion.updatedAt = response.data.updatedAt
      this.getAllTasks(this.currentPage, this.pageSize)

    },
    async getAllTasks(pageNum, pageSize) {
      try {
        const response = await api.get(`/todos`, {
          params: {
            pageNum,
            pageSize
          }
        })
        // assign values from data
        this.total = response.data.total
        this.tasks = response.data.todoList

      } catch (err) {
        console.log(err);
      }
    },
    deleteTask(index) {
      try {
        this.$q.dialog({
          title: 'Confirm',
          message: 'Would you like to delete the task?',
          cancel: true,
        }).onOk(async () => {
          let task_id = this.tasks[index].id
          await api.delete(`/todos/${task_id}`)
          this.tasks.splice(index, 1)
          this.$q.notify('Task deleted!')

          // Update pagination variable
          let totalTasks = (await api.get('/todos')).data.total
          let paginateLength = Math.ceil(totalTasks / this.pageSize)
          this.currentPage = paginateLength
          this.getAllTasks(paginateLength, this.pageSize)
        })
      } catch (err) {
        console.log(err);
      }
    },
    async addTask() {
      let todoData = {
        title: this.newTask,
        done: false
      }
      if (todoData.title === '') {
        this.$q.dialog({
          title: 'Error',
          message: 'Please input task!',
          cancel: true,
        })
      } else {
        try {
          const response = await api.post(`/todos`, todoData)
          todoData.createdAt = response.data.createdAt
          this.tasks.push(todoData)
          this.$q.notify('Task added!')
          this.newTask = ''

          // Update pagination variable
          let totalTasks = (await api.get('/todos')).data.total
          let paginateLength = Math.ceil(totalTasks / this.pageSize)
          this.currentPage = paginateLength
          this.getAllTasks(paginateLength, this.pageSize)

        } catch (err) {
          console.log(err);
        }
      }
    },
    async updateTask(index) {
      try {
        const data = await this.$q.dialog({
          title: 'New task name',
          message: 'Type new task name',
          prompt: {
            model: '',
            type: 'text'
          },
          cancel: true
        }).onOk(async data => {
          if (data === '') {
            return
          } else {
            let todoData = {
              title: data,
              done: false
            }
            let task_id = this.tasks[index].id
            const response = await api.put(`/todos/${task_id}`, todoData)
            todoData.updatedAt = response.data.updatedAt
            this.tasks[index].title = todoData.title
            this.getAllTasks(this.currentPage, this.pageSize)
          }
        })
      } catch (err) {
        console.log(err);
      }
    }
  },

})
</script>

<style lang="scss">
.done {
  .q-item__label {
    text-decoration: line-through;
    color: #bbb;
  }
}

.limit-width {
  max-width: 100vh;
  overflow-wrap: break-word;
}

.no-tasks {
  opacity: 0.5;
}
</style>
