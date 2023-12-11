<template>


          <el-card>
    <el-table :data="pagedTableData" style="width: 100%">
      <el-table-column label="序号" prop="id" />
      <el-table-column label="标题" prop="title" />
      <el-table-column label="发表源" prop="source" />
      <el-table-column label="年份" prop="year" />
      <el-table-column label="类型" prop="type" :formatter="paperLevelFormatter"/>
      <el-table-column label="级别" prop="level" :formatter="paperTypeFormatter"/>
      <el-table-column align="right">
        <template #header>
        <el-input v-model="search" size="small" placeholder="输入论文标题搜索" />
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



    <el-dialog title="作者信息" center v-model='dialogVisible'>
   <el-table
    :data="publication"
    style="width: 100%"
    :row-class-name="tableRowClassName"
  >
    <el-table-column label="工号" prop="workno" />
    <el-table-column label="姓名" prop="name" />
    <el-table-column label="性别" prop="gender" :formatter="genderFormatter" />
    <el-table-column label="级别" prop="level" :formatter="levelFormatter"/>
    <el-table-column label="排名" prop="ranking" />
    <el-table-column label="通讯作者" prop="corresponding" :formatter="correspondingFormatter" />
  </el-table>


    </el-dialog>



</template>

<script setup>
import { computed, ref } from 'vue'
import { Papers, DelPaper,Publications } from '@/api/paper'
import { paper_level_dict,paper_type_dict,levelDict } from '@/utils/dictionary';
import { ElMessageBox } from 'element-plus';


const search = ref('')
const currentPage = ref(1)
const pageSize = ref(5)
const publication = ref([{
   "workno": null,
    "name": null,
    "gender": null,
    "level": null,
    "ranking": null,
    "corresponding": null
}])
// 创建一个响应式变量
const tableData = ref([])
getPapers()

function levelFormatter(row) {
  return levelDict[row.level] ;
}

function paperLevelFormatter(row) {
  return paper_level_dict[row.level] ;
}

function paperTypeFormatter(row) {
  return paper_type_dict[row.type] ;
}

function correspondingFormatter(row) {
  return row.corresponding ? '是' : '否'
}

// 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return tableData.value
  } else {
    return tableData.value.filter(item => item.title.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

function getPapers() {
  // 使用api方法获取论文数据
  Papers().then(res => {
    if (res.data.code === 200) {
      tableData.value = res.data.data.items
    } else {
      alert('论文数据获取失败')
    }
  })
}
const dialogVisible = ref(false)

const handleEdit = (index, row) => {
  Publications(row.id).then(res => {
    if (res.data.code === 200) {
      publication.value = res.data.data.publication
      console.log(publication)
      dialogVisible.value = true // 显示弹窗
    } else {
            ElMessageBox.alert(res.data.msg, '提示', {
            type: 'error'
          }).then(() => {
          })
    }
  })
}


const handleDelete = (index, row) => {
  ElMessageBox.confirm(`确定要删除 论文${row.title} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    DelPaper(row.id).then(res => {
      if (res.data.code === 200) {
        alert('删除成功')
        getPapers()
      } else {
        alert('删除失败')
      }
    })
  }).catch(() => {
    // 用户点击了取消按钮，什么也不做
  });
}


const handleCurrentChange = (current) => {
  currentPage.value = current
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}


const tableRowClassName = ({ row, rowIndex }) => {
  if (rowIndex === 1) {
    return 'warning-row'
  } else if (rowIndex === 3) {
    return 'success-row'
  }
  return ''
}
</script>

<style>
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);

}

</style>