new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],
    data: {
        newTask: '',
        tasks: [],
        markedTasks: [],
    },
    methods: {
        addTask: function(event) {
            console.log('add task');
            event.preventDefault();
            var csrftoken = Cookies.get('csrftoken');
            var data = {"text": this.newTask};
            var self = this;

            $.ajax({
                url: '/api/tasks/',
                type: 'POST',
                data: data,
                headers: { 'X-CSRFToken': csrftoken },
                success: function (result) {
                    self.tasks.push(self.newTask);
                    self.newTask = '';
                },
            });
        },
        removeTask: function (event) {
            console.log('bulk remove tasks');
            event.preventDefault();

            var self = this;
            var data = {
                'ids': this.markedTasks
            };

            $.ajax({
                url: '/api/tasks/bulk_destroy/',
                type: 'DELETE',
                data: data,
                success: function (result) {
                    self.tasks = result['tasks'];
                    self.markedTasks = [];
                },
            });
        },
        removeAll: function (event) {
            console.log('remove all tasks');
            event.preventDefault();
            var self = this;

            $.ajax({
                url: '/api/tasks/destroy_all/',
                type: 'DELETE',
                success: function (result) {
                    self.tasks = [];
                },
            });
        }
    },

    mounted() {
        var self = this;
        $.ajax({
            url: '/api/tasks/',
            type: 'GET',
            success: function (result) {
                self.tasks = result['tasks'];
            }
        });
    }
});