<template>
  <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane label="项目" name="first">
                  <el-card>
      更新项目信息 <br><br>
       <el-form :model="formProject" label-width="120px">

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


         <el-form-item label="项目列表">
             <el-table :data="pagedTableDataProject" style="width: 100%">
      <el-table-column label="项目号" prop="id" />
      <el-table-column label="项目名称" prop="name" />
      <el-table-column label="项目来源" prop="source" />
      <el-table-column label="项目类型" prop="type" />
      <el-table-column label="总经费" prop="totalfund" />
      <el-table-column label="承担经费" prop="fund" />
      <el-table-column label="排名" prop="ranking" />
      <el-table-column label="立项时间" prop="startyear" />
      <el-table-column label="结项时间" prop="endyear" />
      <el-table-column align="right">
        <template #header>
        <el-input v-model="searchProject" size="small" placeholder="输入项目名称搜索" />
      </template>
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :current-page="currentPageProject"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSizeProject"
      :total="filterTableDataProject.length"
      @current-change="handleCurrentChangeProject"
      @size-change="handleSizeChangeProject"
    />

        </el-form-item>

   <el-dialog  title='更新项目信息' center v-model='dialogProjectVisible' >
      <el-form :model="formProjectData" label-width="100px">
        <el-form-item label="项目编号">
          <el-input v-model="formProjectData.id"></el-input>
        </el-form-item>

        <el-form-item label="项目名称">
          <el-input v-model="formProjectData.name"></el-input>
        </el-form-item>

        <el-form-item label="项目来源">
          <el-input v-model="formProjectData.source"></el-input>
        </el-form-item>

        <el-form-item label="项目经费">
          <el-input v-model="formProjectData.totalfund"></el-input>
        </el-form-item>

        <el-form-item label="承担经费">
          <el-input v-model="formProjectData.fund"></el-input>
        </el-form-item>

        <el-form-item label="排名">
          <el-input v-model="formProjectData.ranking"></el-input>
        </el-form-item>


        <el-form-item label="立项时间">
        <el-date-picker
          v-model="formProjectData.startyear"
          type="year"
          placeholder="选择立项时间"
          style="width: 100%"
        />
        </el-form-item>

        <el-form-item label="结项时间">
        <el-date-picker
          v-model="formProjectData.endyear"
          type="year"
          placeholder="选择结项时间"
          style="width: 100%"
        />
        </el-form-item>

        <el-form-item label="项目类型">
          <el-select v-model="formProjectData.type" placeholder="请选择">
            <el-option label="国家级项目" value="1" />
            <el-option label="省部级项目" value="2" />
            <el-option label="市厅级项目" value="3" />
            <el-option label="企业合作项目" value="4" />
            <el-option label="其它类型项目" value="5" />
          </el-select>
        </el-form-item>


      </el-form>
      <div slot="footer" class="dialog-footer" style="display: flex; justify-content: center;">
        <el-button type="primary" @click="handleSave">修改</el-button>
                <el-button @click="cancleProject">取消</el-button>
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
import { UpdateProject } from '@/api/project';
import { levelDict,genderDict } from '@/utils/dictionary';
import { ElMessageBox } from 'element-plus'

const activeName = ref('first')
// 定义响应式变量 ProjectInfo
const projectInfo = ref([])
// 定义响应式变量 teacherOptions
const teacherOptions = ref([])
// 定义响应式变量 selectedCourse，用于显示当前选中的课程信息
const selectedTeacher = ref('')
const search = ref('')
const currentPage = ref(1)
const pageSize = ref(5)

const searchProject = ref('')
const currentPageProject = ref(1)
const pageSizeProject = ref(10)

const formProjectData = ref({
        id: null,
          name: null,
          source: null,
          totalfund: null,
          fund: null,
          ranking: null,
          type: null,
          startyear: null,
          endyear: null,
            workno:null
            })

const dialogProjectVisible = ref(false)

getTeacherOptions()

const handleClick = (tab, event) => {
  console.log(tab, event)
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
const filterTableDataProject = computed(() => {
  const keyword = searchProject.value.trim()
  if (keyword === '') {
    return projectInfo.value
  } else {
    return projectInfo.value.filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )})

  // 创建一个计算属性，用于分页表格数据
const pagedTableDataProject = computed(() => {
  return filterTableDataProject.value.slice(
    (currentPageProject.value - 1) * pageSizeProject.value,
    currentPageProject.value * pageSizeProject.value
  )
})


const handleCurrentChange = (current) => {
  currentPage.value = current
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChangeProject = (current) => {
  currentPageProject.value = current
}

const handleSizeChangeProject = (size) => {
  pageSizeProject.value = size
  currentPageProject.value = 1
}

// do not use same name with ref
const formProject = reactive(
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
  formProject.workno = teacher.workno
  formProject.name = teacher.name
  formProject.gender = teacher.gender
  formProject.level = teacher.level
  // 更新 selectedTeacher 变量，以显示当前选中的课程信息
  selectedTeacher.value = `${teacher.workno} - ${teacher.name}`

  teacherInfo().then(res => {
      if (res.data.code === 200) {
       const  targetItem = res.data.data.items.find(item => item.workno === teacher.workno);
                     if (targetItem.projectInfo[0] == null || !targetItem.projectInfo[0]["name"]) {
                alert('这个老师的项目信息似乎是空的~');
              } if (targetItem) {
             projectInfo.value = targetItem.projectInfo;

          } else {
           alert('找不到指定工号的论文信息')
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
  formProjectData.value = { ...row }
  formProjectData.value.workno = formProject.workno
  formProjectData.value.originId = formProjectData.value.id
  formProjectData.value.originFund = formProjectData.value.fund
  formProjectData.value.startyear = new Date(formProjectData.value.startyear, 0, 1);
  formProjectData.value.endyear = new Date(formProjectData.value.endyear, 0, 1);
  dialogProjectVisible.value = true
}

function handleSave() {
  console.log(formProjectData)

    UpdateProject(formProjectData)
  .then(res => {
    if (res.data.code === 200) {
          ElMessageBox.alert(res.data.msg, '提示', {
            confirmButtonText: '确定',
            type: 'success'
          }).then(() => {
             dialogProjectVisible.value = false
          selectTeacher(formProject);
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

function cancleProject(){
  dialogProjectVisible.value = false
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
