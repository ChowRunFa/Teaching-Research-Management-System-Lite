<template>
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
          <el-tab-pane label="教师信息" name="first">
                  <el-card>
             <el-table :data="pagedTableData" style="width: 100%">
      <el-table-column label="工号" prop="workno" />
      <el-table-column label="姓名" prop="name" />
      <el-table-column label="性别" prop="gender" :formatter="formatGender"/>
      <el-table-column label="职称" prop="level" :formatter="levelFormatter"/>
      <el-table-column align="right">
        <template #header>
        <el-input v-model="search" size="small" placeholder="输入教师姓名搜索" />
      </template>
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">查看</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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

                  </el-card>
          </el-tab-pane>

                <el-tab-pane label="新建教师信息" name="second">
                  <el-card>
      新建教师信息 <br><br>
       <el-form :model="form" label-width="120px">
    <el-form-item label="教师工号">
      <el-input v-model="form.workno"  placeholder="输入教师工号"/>
    </el-form-item>

         <el-form-item label="教师姓名">
      <el-input v-model="form.name" placeholder="输入教师姓名"/>
    </el-form-item>

         <el-form-item label="教师性别">
<el-select v-model="form.gender" placeholder="选择教师性别">
  <el-option label="男" value="1" />
  <el-option label="女" value="2" />
  <el-option label="武装直升机" value="3" />
  <el-option label="沃尔玛购物袋" value="4" />
  <el-option label="其他" value="5" />
      </el-select>
    </el-form-item>

    <el-form-item label="教师职称">
      <el-select v-model="form.level" placeholder="选择教师职称">
  <el-option label="博士后" value="1" />
  <el-option label="助教" value="2" />
  <el-option label="讲师" value="3" />
  <el-option label="副教授" value="4" />
  <el-option label="特任教授" value="5" />
  <el-option label="教授" value="6" />
  <el-option label="助理研究员" value="7" />
  <el-option label="特任副研究员" value="8" />
  <el-option label="副研究员" value="9" />
  <el-option label="特任研究员" value="10" />
  <el-option label="研究员" value="11" />
      </el-select>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">创建</el-button>
      <el-button>取消</el-button>
    </el-form-item>
  </el-form>
                          </el-card>
          </el-tab-pane>
    </el-tabs>

</template>

<script setup>
import { computed,reactive ,ref } from 'vue'
import { Teachers, NewTeacher } from '@/api/teacher'
import { levelDict,genderDict } from '@/utils/dictionary';

const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const activeName = ref('first')
// 创建一个响应式变量
const tableData = ref([])
getTeachers()

// 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return tableData.value
  } else {
    return tableData.value.filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

const form = reactive(
    {
      workno: null,
      name: null,
      gender: null,
      level: null
    })




function getTeachers() {
  // 使用api方法获取论文数据
  Teachers().then(res => {
    if (res.data.code === 200) {
      tableData.value = res.data.data.items
    } else {
      alert('教师数据获取失败')
    }
  })
}

const handleClick = (tab, event) => {
  console.log(tab, event)
}

const handleEdit = (index, row) => {
  console.log(index, row)
}

function formatGender(row) {
  return genderDict[row.gender];
}

function levelFormatter(row) {
  return levelDict[row.level] ;
}

const handleDelete = (index, row) => {
  console.log(index, row)
  alert("危险操作！你干嘛！")
  // DelCourse(row.id).then(res => {
  //   if (res.data.code === 200) {
  //     alert('删除成功')
  //     getCourses()
  //   } else {
  //     alert('删除失败')
  //   }
  // })
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const onSubmit = () => {
        console.log(form)
        // console.log(data.corresponding_author)
  NewTeacher(form)
  .then(res => {
    if (res.data.code === 200) {
           alert(res.data.msg)
  }else {
           alert(res.data.msg)
    }
  })
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