<template>
  <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane label="课程" name="first">
                  <el-card>
      更新论文信息 <br><br>
       <el-form :model="formPaper" label-width="120px">

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

         <el-form-item label="论文列表">
             <el-table :data="pagedTableDataPaper" style="width: 100%">
  <el-table-column label="序号" prop="id" />
  <el-table-column label="标题" prop="title" />
  <el-table-column label="发表源" prop="source" />
  <el-table-column label="类型" prop="type" />
  <el-table-column label="年份" prop="year" />
  <el-table-column label="级别" prop="level" />
  <el-table-column label="排名" prop="ranking" />
  <el-table-column label="通讯作者" prop="corresponding" :formatter="formatCorresponding" />
      <el-table-column align="right">
        <template #header>
        <el-input v-model="searchPaper" size="small" placeholder="输入论文标题搜索" />
      </template>
        <template #default="scope">
          <el-button size="small"  @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :current-page="currentPagePaper"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSizePaper"
      :total="filterTableDataPaper.length"
      @current-change="handleCurrentChangePaper"
      @size-change="handleSizeChangePaper"
    />

        </el-form-item>

   <el-dialog  title='更新论文信息' center v-model='dialogPaperVisible' >
      <el-form :model="formPaperData" label-width="100px">
        <el-form-item label="序号">
          <el-input type="number" min="0" v-model="formPaperData.id"></el-input>
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="formPaperData.title"></el-input>
        </el-form-item>
        <el-form-item label="发表源">
          <el-input v-model="formPaperData.source"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="formPaperData.type" placeholder="请选择">
      <el-option label="full paper" value="1" />
      <el-option label="short paper" value="2" />
      <el-option label="poster paper" value="3" />
      <el-option label="demo paper" value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="年份">
        <el-date-picker
          v-model="formPaperData.year"
          type="date"
          placeholder="选择论文发表时间"
          style="width: 100%"
        />
        </el-form-item>
        <el-form-item label="级别">
          <el-select v-model="formPaperData.level" placeholder="请选择">
      <el-option label="CCF-A" value="1" />
      <el-option label="CCF-B" value="2" />
      <el-option label="CCF-C" value="3" />
      <el-option label="中文CCF-A" value="4" />
      <el-option label="中文CCF-B" value="5" />
      <el-option label="无级别" value="6" />
          </el-select>
        </el-form-item>
        <el-form-item label="排名">
          <el-input type="number" min="1" v-model="formPaperData.ranking"></el-input>
        </el-form-item>
        <el-form-item label="通讯作者">
          <el-switch   v-model="formPaperData.corresponding" active-value=true inactive-value=false ></el-switch>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" style="display: flex; justify-content: center;">
        <el-button type="primary" @click="handleSave">修改</el-button>
                <el-button @click="cancle">取消</el-button>
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
import { computed,ref  } from 'vue'
import { reactive } from 'vue'
import {Teachers} from '@/api/teacher'
import { teacherInfo } from '@/api/user';
import { UpdatePaper } from '@/api/paper';
import { levelDict,genderDict } from '@/utils/dictionary';
import { ElMessageBox } from 'element-plus'

const activeName = ref('first')
// 定义响应式变量 paperInfo
const paperInfo = ref([])
// 定义响应式变量 teacherOptions
const teacherOptions = ref([])
// 定义响应式变量 selectedCourse，用于显示当前选中的课程信息
const selectedTeacher = ref('')
const search = ref('')
const currentPage = ref(1)
const pageSize = ref(5)

const searchPaper = ref('')
const currentPagePaper = ref(1)
const pageSizePaper = ref(10)

const formPaperData = ref({
                  id: null,
                title: null,
                source: null,
                type: null,
                year: null,
                level: null,
                ranking: null,
                corresponding: null,
                workno: null,
                originId: null
            })

const dialogPaperVisible = ref(false)


getTeacherOptions()

const handleClick = (tab, event) => {
  console.log(tab, event)
}

function cancle(){

  dialogPaperVisible.value = false;

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
const filterTableDataPaper = computed(() => {
  const keyword = searchPaper.value.trim()
  if (keyword === '') {
    return paperInfo.value
  } else {
    return paperInfo.value.filter(item => item.title.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )})

  // 创建一个计算属性，用于分页表格数据
const pagedTableDataPaper = computed(() => {
  return filterTableDataPaper.value.slice(
    (currentPagePaper.value - 1) * pageSizePaper.value,
    currentPagePaper.value * pageSizePaper.value
  )
})


const handleCurrentChange = (current) => {
  currentPage.value = current
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChangePaper = (current) => {
  currentPagePaper.value = current
}

const handleSizeChangePaper = (size) => {
  pageSizePaper.value = size
  currentPagePaper.value = 1
}

// do not use same name with ref
const formPaper = reactive(
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
        alert("教师数据获取失败")
      }
    })
}

// 处理选择课程的事件
const selectTeacher = (teacher) => {
  formPaper.workno = teacher.workno
  formPaper.name = teacher.name
  formPaper.gender = teacher.gender
  formPaper.level = teacher.level
  // 更新 selectedTeacher 变量，以显示当前选中的课程信息
  selectedTeacher.value = `${teacher.workno} - ${teacher.name}`

  teacherInfo().then(res => {
      if (res.data.code === 200) {
       const  targetItem = res.data.data.items.find(item => item.workno === teacher.workno);
                     if (targetItem.paperInfo[0] == null || !targetItem.paperInfo[0]["title"]) {
                alert('这个老师的论文信息似乎是空的~');
              } if (targetItem) {
             paperInfo.value = targetItem.paperInfo;
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
  formPaperData.value = { ...row }
  formPaperData.value.workno = formPaper.workno
  formPaperData.value.originId = formPaperData.value.id
  dialogPaperVisible.value = true
}

function handleSave() {
  console.log(formPaperData)

    UpdatePaper(formPaperData)
  .then(res => {
    if (res.data.code === 200) {
          ElMessageBox.alert(res.data.msg, '提示', {
            confirmButtonText: '确定',
            type: 'success'
          }).then(() => {
             dialogPaperVisible.value = false
          selectTeacher(formPaper);
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

 function formatCorresponding(row) {
  return row.corresponding ? "是" : "否"
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
