<style scoped>
.el-row{
  height: 100%;
}

.el-menu{
  border-right: 1px solid #f5f1f1;
}
.el-aside{
  border-right: 1px solid #f5f1f1;
}
</style>

<template>
  <el-aside width="200px">
    <el-row class="tac">
      <el-col>
        <el-menu
          default-active="1"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
        >
          <el-menu-item index="1" @click="goPage('teacherinfo')">
            <el-icon><View /></el-icon>
            <span slot="title">信息总览</span>
          </el-menu-item>

          <el-menu-item index="2" @click="goPage('manage')">
            <el-icon><Tickets /></el-icon>
            <span slot="title">论文登记</span>
          </el-menu-item>

          <el-menu-item index="3" @click="goPage('addproject')">
            <el-icon><TakeawayBox /></el-icon>
            <span slot="title">项目登记</span>
          </el-menu-item>

          <el-menu-item index="4" @click="goPage('addcourse')">
            <el-icon><Reading /></el-icon>
            <span slot="title">课程登记</span>
          </el-menu-item>

          <el-menu-item index="5" @click="goPage('teacher')">
           <el-icon><User /></el-icon>
            <span slot="title">教师信息</span>
          </el-menu-item>

          <el-menu-item index="6" @click="goPage('paper')">
          <el-icon><Collection /></el-icon>
            <span slot="title">论文信息</span>
          </el-menu-item>

          <el-menu-item index="7" @click="goPage('project')">
            <el-icon><MessageBox /></el-icon>
            <span slot="title">项目信息</span>
          </el-menu-item>

          <el-menu-item index="8" @click="goPage('course')">
          <el-icon><Document /></el-icon>
            <span slot="title">课程信息</span>
          </el-menu-item>

          <el-menu-item index="9" @click="goPage('updatePaper')">
            <el-icon><Edit /></el-icon>
            <span slot="title">论文更新</span>
          </el-menu-item>

          <el-menu-item index="10" @click="goPage('updateProject')">
            <el-icon><MessageBox /></el-icon>
            <span slot="title">项目更新</span>
          </el-menu-item>

          <el-menu-item index="11" @click="goPage('updateCourse')">
            <el-icon><Crop /></el-icon>
            <span slot="title">课程更新</span>
          </el-menu-item>

          <el-menu-item index="12" @click="goPage('teacherRank')">
            <el-icon><DataAnalysis /></el-icon>
            <span slot="title">文章分布</span>
          </el-menu-item>

          <el-menu-item index="13" @click="goPage('paperCount')">
            <el-icon><Histogram /></el-icon>
            <span slot="title">发文趋势</span>
          </el-menu-item>

          <el-menu-item index="14" @click="goPage('projectPie')">
            <el-icon><PieChart /></el-icon>
            <span slot="title">项目分布</span>
          </el-menu-item>

          <el-menu-item index="15" @click="goPage('projectLine')">
            <el-icon><DataLine /></el-icon>
            <span slot="title">项目趋势</span>
          </el-menu-item>

          <el-menu-item index="16" @click="goPage('teacherCompare')">
            <el-icon><Rank /></el-icon>
            <span slot="title">教师对比</span>
          </el-menu-item>

          <el-menu-item index="17" @click="goPage('courseScatter')">
            <el-icon><SetUp /></el-icon>
            <span slot="title">课程安排</span>
          </el-menu-item>

          <el-menu-item index="18" @click="goPage('courseStack')">
            <el-icon><Files /></el-icon>
            <span slot="title">课程分布</span>
          </el-menu-item>

        </el-menu>
      </el-col>
    </el-row>
  </el-aside>
</template>

<script>
var $this = {};
 import {
   Location, Setting, Menu ,Document,ChatDotSquare,View,SetUp,Rank,TakeawayBox,PieChart,Histogram,Files,
  Tickets, DataAnalysis, Reading, User, Collection, DataLine,Edit,MessageBox,Crop} from '@element-plus/icons'
export default {
  components: {
            Location, Setting, Menu ,Document,ChatDotSquare,View,SetUp,Rank,TakeawayBox,PieChart,Histogram,Files,
  Tickets, DataAnalysis, Reading, User, Collection, DataLine,Edit,MessageBox,Crop
        },
  data() {
    return {};
  },
  beforeCreate() {
    $this = this;
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },

    goPage(link) {
      if (link === "teacherinfo") {
        $this.$router.push("/admin/teacherinfo").catch(error => error);
      } else if (link === "manage") {
        $this.$router.push("/admin/manage").catch(error => error);
      } else if (link === "addproject") {
        $this.$router.push("/admin/addproject").catch(error => error);
      } else if (link === "addcourse") {
        $this.$router.push("/admin/addcourse").catch(error => error);
      } else if (link === "teacher") {
        $this.$router.push("/admin/teacher").catch(error => error);
      } else if (link === "paper") {
        $this.$router.push("/admin/paper").catch(error => error);
      }else if (link === "project") {
        $this.$router.push("/admin/project").catch(error => error);
      }else if (link === "course") {
        $this.$router.push("/admin/course").catch(error => error);
      }else if (link === "updatePaper") {
        $this.$router.push("/admin/updatePaper").catch(error => error);
      }else if (link === "updateProject") {
        $this.$router.push("/admin/updateProject").catch(error => error);
      }else if (link === "updateCourse") {
        $this.$router.push("/admin/updateCourse").catch(error => error);
      } else if (link === "teacherRank") {
        $this.$router.push("/admin/teacherRank").catch(error => error);
      }else if (link === "paperCount") {
        $this.$router.push("/admin/paperCount").catch(error => error);
      }else if (link === "projectPie") {
        $this.$router.push("/admin/projectPie").catch(error => error);
      }else if (link === "teacherCompare") {
        $this.$router.push("/admin/teacherCompare").catch(error => error);
      }else if (link === "courseScatter") {
        $this.$router.push("/admin/courseScatter").catch(error => error);
      }else if (link === "courseStack") {
        $this.$router.push("/admin/courseStack").catch(error => error);
      }else if (link === "projectLine") {
        $this.$router.push("/admin/projectLine").catch(error => error);
      } else {

      }
    }
  }



};
</script>
