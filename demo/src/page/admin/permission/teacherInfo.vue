<template>

  <div class="container">
      <el-main>
    <el-card>
       <el-form :model="formTeacherInfo" label-width="120px">
          <el-row>
            <el-col :span="8">
              <el-date-picker
                  v-model="formTeacherInfo.startYear"
                  type="year"
                  placeholder="开始年份"
                  @change="updateForm('startYear', $event)"
              />
            </el-col>
            <el-col :span="8">
              <el-date-picker
                  v-model="formTeacherInfo.endYear"
                  type="year"
                  placeholder="结束年份"
                  @change="updateForm('endYear', $event)"
              />
            </el-col>
            <!-- 添加一个开关，选择是否根据时间选择 -->
            <el-col :span="8">
     <el-switch
         v-model="showYearPicker"
         inline-prompt
        active-text="指定时间"
        inactive-text="所有时间"
         @change="judge">
     </el-switch>

          </el-col>
          </el-row>
                    </el-form>


    <el-table :data="pagedTableData" style="width: 100%" @row-click="selectOneTeacher" >
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="gender" label="性别">
        <template #default="{ row }">
          {{ row.gender === 1 ? "男" : "女" }}
        </template>
      </el-table-column>
      <el-table-column prop="level" label="职称"></el-table-column>
      <el-table-column prop="workno" label="工号"></el-table-column>
              <el-table-column label="操作">
          <template #header>
        <el-input v-model="search" size="default" placeholder="输入教师名称搜索"  style="width: 100%;"/>
      </template>
          <template v-slot="scope">
            <el-button type="text" >查看</el-button>
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
  </el-main>


<el-container v-if="selectedInfoTeacher">
  <el-main>
    <el-card>
      <div  class="teacher-details" id="teacher-details-container">
        <div class="section">
          <h1 class="section-title">教学科研情况 </h1>
          <h3 class="section-subtitle" v-if="showYearPicker">{{ getYearString(formTeacherInfo.startYear) }}至{{ getYearString(formTeacherInfo.endYear)}}年</h3>
              <div style="display: flex; justify-content: flex-end;">
      <el-button type="primary" @click="printPDF"><el-icon><Download /></el-icon></el-button>
    </div>
          <div class="section-content">
            <div class="subsection">
              <h2 class="subsection-title">个人信息</h2>
                          <hr class="divider">

<div   style="display: flex;">
  <table class="teacher-info" style="margin-right:20px;">
    <tr>
      <th><a class="detail-info">姓名</a></th>
      <td><a class="detail-info">{{ selectedInfoTeacher.name }}</a></td>
    </tr>
  </table>
  <table class="teacher-info" style="margin-right:20px;">
    <tr>
      <th><a class="detail-info">性别</a></th>
      <td><a class="detail-info">{{ selectedInfoTeacher.gender === 1 ? "男" : "女" }}</a></td>
    </tr>
  </table>
  <table class="teacher-info" style="margin-right:20px;">
    <tr>
      <th><a class="detail-info">职称</a></th>
      <td><a class="detail-info">{{ selectedInfoTeacher.level }}</a></td>
    </tr>
  </table>
  <table class="teacher-info" style="margin-right:20px;">
    <tr>
      <th><a class="detail-info">工号</a></th>
      <td><a class="detail-info">{{ selectedInfoTeacher.workno }}</a></td>
    </tr>
  </table>
</div>
            </div>
            <div class="subsection">
              <h2 class="subsection-title">教学情况</h2>
                          <hr class="divider">
               <ol class="centered-list">
                <li v-for="(course, index) in selectedInfoTeacher.courseInfo" :key="index">
                  <a  class="detail-info"> 课程号：{{ course.id }}，《{{ course.name }}》,{{course.year}}年 {{course.semester}}，总学时：{{ course.hours }}，主讲学时：{{ course.parthours }}，性质：{{course.property}}</a>
                </li>
              </ol>
            </div>
            <div class="subsection">
              <h2 class="subsection-title">论文发表情况</h2>
                          <hr class="divider">
               <ol class="centered-list">
                <li v-for="(paper, index) in selectedInfoTeacher.paperInfo" :key="index">
                 <a  class="detail-info"> "{{ paper.title }}"，{{ paper.source }}，{{ paper.year }}，{{ paper.level }}，排名第{{paper.ranking}}</a>
                 <a v-if="paper.corresponding" class="detail-info">，通讯作者</a>
                </li>
              </ol>
            </div>

            <div class="subsection">
              <h2 class="subsection-title">项目承担情况</h2>
                          <hr class="divider">
               <ol class="centered-list">
                <li v-for="(project, index) in selectedInfoTeacher.projectInfo" :key="index">
                  <a class="detail-info"> "{{ project.name }}". {{ project.source }}. {{ project.startyear }}-{{ project.endyear }} {{ project.type }} 总经费：{{project.totalfund}} 承担经费：{{project.fund}}</a>
                </li>
              </ol>
            </div>
          </div>
        </div>
<div style="display: flex; justify-content: center;">
  <el-button @click="clearInfo">关闭</el-button>
</div>
      </div>
    </el-card>
  </el-main>
</el-container>



  </div>
</template>

<script setup>
import { reactive,watch, computed, ref } from "vue";
import {teacherInfo, yearInfo} from "@/api/user"
import {Download} from '@element-plus/icons'

const search = ref('')
const currentPage = ref(1)
const pageSize = ref(5)
const items = ref([])
// const items = reactive([])
const showYearPicker = ref(false);


const formTeacherInfo = reactive({
    startYear:null,
    endYear:null
    })

function updateForm(name, event) {
  formTeacherInfo[name] = event;
}
function clearInfo() {
selectedInfoTeacher.value =  null;
}

    getInfo();

// 监控showYearPicker变量的变化，根据其值和时间选择情况调用不同的数据获取方法
watch(showYearPicker, (newValue) => {
  if (newValue) {
    if (!formTeacherInfo.endYear || !formTeacherInfo.startYear) {
      showYearPicker.value = false;
      alert('请先选择起始时间和结束时间');
    }else {
          getInfo();
    }
  }else {
    getInfo();
  }
})

 function getYearString(timestamp) {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      const year = date.getFullYear()
      return year.toString()
    }

function getInfo() {
  // 使用api方法获取数据
  if (showYearPicker.value) {
        yearInfo(formTeacherInfo).then(res => {
      if (res.data.code === 200) {
        items.value = res.data.data.items;
        console.log(formTeacherInfo)
      } else {
        alert('数据获取失败')
      }
    })
  }else {
    teacherInfo().then(res => {
      if (res.data.code === 200) {
        items.value = res.data.data.items
      } else {
        alert('数据获取失败')
      }
    })
  }
}



  const selectedInfoTeacher = ref(null);
  // const selectedInfoTeacher = reactive(null);
    function selectOneTeacher(infoTeacher) {
      console.log(infoTeacher);
      selectedInfoTeacher.value = infoTeacher;
    }

    // 创建一个计算属性，用于过滤表格数据
const filterTableData = computed(() => {
  const keyword = search.value.trim()
  if (keyword === '') {
    return items.value
  } else {
    return items.value.filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
  }
})

// 创建一个计算属性，用于分页表格数据
const pagedTableData = computed(() => {
  return filterTableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

const handleCurrentChange = (current) => {
  currentPage.value = current
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

 const printPDF = () => {
  // 定义打印样式
  let printStyle = `
    <style>
      @media print {
        #teacher-details-container {
          position: static !important;
        }
        .el-button {
          display: none !important;
        }
      }

.section {
  margin-top: 30px;
  margin-bottom: 30px;
}
p{
            margin:1em 0;
            padding:0 0 0 2em;
            text-indent:-1.5em;
            font:normal normal 16px/1.6em SimSun-ExtB;
            color:#000;
        }

.section-title {
  text-align: center;
  font-size: 30px;
  font-weight: bold;
    font-family: SimSun-ExtB,serif;
}

.section-subtitle {
    text-align: center;
  font-size: 25px;
  font-weight: bold;
  font-family: SimSun-ExtB,serif;
}

.section-content {
  padding: 20px;
}

.subsection {
  margin-top: 20px;
  margin-bottom: 20px;
}

.subsection-title {
  font-size: 24px;
  font-weight: bold;
    font-family: SimSun-ExtB,serif;
}

.divider {
  border: none;
  border-top: 1px solid #ccc;
  margin-top: 30px;
  margin-bottom: 30px;
}

.centered-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 10px;
}
.detail-info{
  font-size: 15px;
    font-family: STXihei,sans-serif;
}
.centered-list li {
  text-align: center;
  padding: 5px;
}


.teacher-info {
  border-collapse: collapse;
}
.teacher-info th, .teacher-info td {
  border: 1px solid black;
  padding: 8px;
}
.teacher-info th {
  background-color: #f2f2f2;
}
    </style>
  `;

  // 获取<el-container>的HTML内容
  let containerHtml = document.getElementById('teacher-details-container').innerHTML;

  // 创建一个新的窗口，打印HTML内容
let printWindow = window.open('www.xxx.com', '_blank');
  printWindow.document.write(printStyle + containerHtml);
  printWindow.print();
  printWindow.close();
}


</script>

<style>
.container {
  margin: 20px;
}

.section {
  margin-top: 30px;
  margin-bottom: 30px;
}
p{
            margin:1em 0;
            padding:0 0 0 2em;
            text-indent:-1.5em;
            font:normal normal 16px/1.6em SimSun-ExtB;
            color:#000;
        }

.section-title {
  text-align: center;
  font-size: 30px;
  font-weight: bold;
    font-family: SimSun-ExtB,serif;
}

.section-subtitle {
    text-align: center;
  font-size: 25px;
  font-weight: bold;
  font-family: SimSun-ExtB,serif;
}

.section-content {
  padding: 20px;
}

.subsection {
  margin-top: 20px;
  margin-bottom: 20px;
}

.subsection-title {
  font-size: 24px;
  font-weight: bold;
    font-family: SimSun-ExtB,serif;
}

.divider {
  border: none;
  border-top: 1px solid #ccc;
  margin-top: 30px;
  margin-bottom: 30px;
}

.centered-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 10px;
}
.detail-info{
  font-size: 15px;
    font-family: STXihei,sans-serif;
}
.centered-list li {
  text-align: center;
  padding: 5px;
}


.teacher-info {
  border-collapse: collapse;
}
.teacher-info th, .teacher-info td {
  border: 1px solid black;
  padding: 8px;
}
.teacher-info th {
  background-color: #f2f2f2;
}
</style>