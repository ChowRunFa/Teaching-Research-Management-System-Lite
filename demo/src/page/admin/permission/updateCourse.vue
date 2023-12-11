<template>
  <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane label="课程" name="first">
                  <el-card>
      更新课程信息 <br><br>
       <el-form :model="formCourse" label-width="120px">

          <!-- 选择课程表格 -->
    <el-form-item label="选择教师">

      <el-table :data="pagedTableData" style="width: 100%">
      <el-table-column label="工号" prop="workno" />
      <el-table-column label="姓名" prop="name" />
      <el-table-column label="性别" prop="gender" :formatter="genderFormatter"/>
      <el-table-column label="职称" prop="level" :formatter="levelFormatter"/>
        <el-table-column label="操作">
          <template #header>
        <el-input v-model="search" size="default" placeholder="输入教师名搜索"  style="width: 50%;"/>
      </template>
          <template v-slot="scope">
            <el-button type="text" @click="selectTeacher(scope.row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>

<el-pagination
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize"
      :total="filterTableData.length"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    />

    </el-form-item>

             <!-- 显示当前选中的课程 -->
    <el-form-item label="当前选中的教师">
      <el-input v-model="selectedTeacher" disabled></el-input>
    </el-form-item>


         <el-form-item label="课程列表">
             <el-table :data="pagedTableDataCourse" style="width: 100%">
  <el-table-column label="课程号" prop="id" />
  <el-table-column label="课程名" prop="name" />
  <el-table-column label="总学时" prop="hours" />
  <el-table-column label="承担学时" prop="parthours" />
  <el-table-column label="学年" prop="year" />
  <el-table-column label="学期" prop="semester" />
  <el-table-column label="性质" prop="property"  />
      <el-table-column align="right">
        <template #header>
        <el-input v-model="searchCourse" size="small" placeholder="输入课程名搜索" />
      </template>
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :current-page="currentPageCourse"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSizeCourse"
      :total="filterTableDataCourse.length"
      @current-change="handleCurrentChangeCourse"
      @size-change="handleSizeChangeCourse"
    />

        </el-form-item>

   <el-dialog  title='更新课程信息' center v-model='dialogVisibleCourse' >
      <el-form :model="formCourseData" label-width="100px">
        <el-form-item label="课程号">
          <el-input v-model="formCourseData.id"></el-input>
        </el-form-item>
        <el-form-item label="课程名">
          <el-input v-model="formCourseData.name"></el-input>
        </el-form-item>
        <el-form-item label="总学时">
          <el-input v-model="formCourseData.hours"></el-input>
        </el-form-item>
        <el-form-item label="承担学时">
          <el-input v-model="formCourseData.parthours"></el-input>
        </el-form-item>
                <el-form-item label="学年">
        <el-date-picker
          v-model="formCourseData.year"
          type="year"
          placeholder="选择课程学年"
          style="width: 100%"
        />
        </el-form-item>
          <el-form-item label="学期">
    <el-select v-model="formCourseData.semester" placeholder="选择课程学期" @change="handleSelectChange">
          <el-option label="春季学期" value="1" />
          <el-option label="夏季学期" value="2" />
          <el-option label="秋季学期" value="3" />
    </el-select>
          </el-form-item>
        <el-form-item label="性质">
          <el-select v-model="formCourseData.property" placeholder="选择课程性质">
      <el-option label="必修" value="1" />
      <el-option label="选修" value="2" />
      <el-option label="公选" value="3" />
      <el-option label="通识" value="4" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" style="display: flex; justify-content: center;">
        <el-button type="primary" @click="handleSaveCourse">修改</el-button>
                <el-button @click="cancleCourse">取消</el-button>
      </div>
    </el-dialog>



         <!--    <el-form-item>-->
<!--      <el-button type="primary" @click="onSubmit">提交</el-button>-->
<!--      <el-button>取消</el-button>-->
<!--    </el-form-item>-->

  </el-form>
                    </el-card>
    </el-tab-pane>

  </el-tabs>
</template>
<script  setup>
import { computed,ref } from 'vue'
import { reactive } from 'vue'
import {Teachers} from '@/api/teacher'
import { teacherInfo } from '@/api/user';
import { levelDict,genderDict } from '@/utils/dictionary';
import { UpdateCourse } from '@/api/course';
import { ElMessageBox } from 'element-plus'

const activeName = ref('first')
// 定义响应式变量 courseInfo
const courseInfo = ref([])
// 定义响应式变量 teacherOptions
const teacherOptions = ref([])
// 定义响应式变量 selectedCourse，用于显示当前选中的课程信息
const selectedTeacher = ref('')
const search = ref('')
const currentPage = ref(1)
const pageSize = ref(5)

const searchCourse = ref('')
const currentPageCourse = ref(1)
const pageSizeCourse = ref(10)

const formCourseData = ref({
        id: null,
        name: null,
        hours: null,
        property: null,
        semester: null,
        year: null,
        parthours: null
            })

const dialogVisibleCourse = ref(false)

getTeacherOptions()

const handleClick = (tab, event) => {
  console.log(tab, event)
}
function cancleCourse(){
  dialogVisibleCourse.value = false;
}

// 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return teacherOptions.value
  } else {
    return teacherOptions.value.filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于过滤表格数据
const filterTableDataCourse = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return courseInfo.value
  } else {
    return courseInfo.value.filter(item => item.title.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )})

  // 创建一个计算属性，用于分页表格数据
const pagedTableDataCourse = computed(() => {
  return filterTableDataCourse.value.slice(
    (currentPageCourse.value - 1) * pageSizeCourse.value,
    currentPageCourse.value * pageSizeCourse.value
  )
})


const handleCurrentChange = (current) => {
  currentPage.value = current
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChangeCourse = (current) => {
  currentPageCourse.value = current
}

const handleSizeChangeCourse = (size) => {
  pageSizeCourse.value = size
  currentPageCourse.value = 1
}

// do not use same name with ref
const formCourse = reactive(
    {
      workno: null,
      name: null,
      gender: null,
      level: null
    })

function getTeacherOptions() {
  // 使用 Teachers API 获取课程列表
  Teachers()
    .then(res => {
      if (res.data.code === 200) {
        teacherOptions.value = res.data.data.items
      } else {
        alert("课教师数据获取失败")
      }
    })
}

// 处理选择课程的事件
const selectTeacher = (teacher) => {
  // 将课程信息填充到表单中
  formCourse.workno = teacher.workno
  formCourse.name = teacher.name
  formCourse.gender = teacher.gender
  formCourse.level = teacher.level
  // 更新 selectedTeacher 变量，以显示当前选中的课程信息
  selectedTeacher.value = `${teacher.workno} - ${teacher.name}`

  teacherInfo().then(res => {
      if (res.data.code === 200) {
       const  targetItem = res.data.data.items.find(item => item.workno === teacher.workno);
                     if (targetItem.courseInfo[0] == null || !targetItem.courseInfo[0]["name"]) {
                alert('这个老师的课程信息似乎是空的~');
              } if (targetItem) {
             courseInfo.value = targetItem.courseInfo;
          } else {
           alert('找不到指定工号的课程信息')
          }
      } else {
        alert(res.data.msg)
      }
    })
}


// 创建一个响应式变量
var worknoOptions = ref([]);
getTeachers();

function getTeachers() {
    // 使用api方法
    Teachers()
        .then(res => {
            if (res.data.code === 200) {
                worknoOptions.value = res.data.data.items;
            } else {
                alert("教师数据获取失败");
            }
        })
}

function handleEdit(index, row) {
  // 将选择的行数据保存到表单数据中
  console.log(index, row)
  formCourseData.value = { ...row }
  formCourseData.value.workno = formCourse.workno
  formCourseData.value.year = new Date(formCourseData.value.year, 0, 1);
  formCourseData.value.originId = formCourseData.value.id
  formCourseData.value.originHours = formCourseData.value.hours
  formCourseData.value.originPartHours = formCourseData.value.parthours
  dialogVisibleCourse.value = true
}

function handleSaveCourse() {
  console.log(formCourseData)
  UpdateCourse(formCourseData)
  .then(res => {
    if (res.data.code === 200) {
          ElMessageBox.alert(res.data.msg, '提示', {
            confirmButtonText: '确定',
            type: 'success'
          }).then(() => {
             dialogVisibleCourse.value = false
          selectTeacher(formCourse);
          })
  }else {
      ElMessageBox.alert(res.data.msg, '提示', {
            confirmButtonText: '确定',
            type: 'error'
          }).then(() => {
          })
    }
  })
}

function genderFormatter(row) {
  return genderDict[row.gender] ;
}

function levelFormatter(row) {
  return levelDict[row.level] ;
}


</script>
<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>
