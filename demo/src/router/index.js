import {createRouter,createWebHashHistory} from "vue-router"

const routes = [
    {//登录
        path:'/',
        name:'login',
        component:()=>import(/*webpackChunkName:'Login'*/'@/page/login/login')
    },
    {
        path: '/admin',
        name: 'admin',
        component:()=>import(/*webpackChunkName:'manage'*/'@/page/admin/layout'),
        children:[
            {
                name:'teacherinfo',
                path:'/admin/teacherinfo',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/teacherInfo')
            },
            {
                name:'manage',
                path:'/admin/manage',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/manage')
            },
            {
                name:'addproject',
                path:'/admin/addproject',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/addProject')
            },
            {
                name:'addcourse',
                path:'/admin/addcourse',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/addCourse')
            },
            {
                name:'teacher',
                path:'/admin/teacher',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/teacher')
            },
            {
                name:'paper',
                path:'/admin/paper',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/paper')
            },
            {
                name:'project',
                path:'/admin/project',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/project')
            },
            {
                name:'course',
                path:'/admin/course',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/course')
            },
            {
                name:'updatePaper',
                path:'/admin/updatePaper',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/updatePaper')
            },
            {
                name:'updateProject',
                path:'/admin/updateProject',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/updateProject')
            },
            {
                name:'updateCourse',
                path:'/admin/updateCourse',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/permission/updateCourse')
            },
            {
                name:'teacherRank',
                path:'/admin/teacherRank',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/visualization/teacherRank')
            },
            {
                name:'paperCount',
                path:'/admin/paperCount',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/visualization/paperCount')
            },
            {
                name:'projectPie',
                path:'/admin/projectPie',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/visualization/projectPie')
            },
            {
                name:'teacherCompare',
                path:'/admin/teacherCompare',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/visualization/teacherCompare')
            },
            {
                name:'courseScatter',
                path:'/admin/courseScatter',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/visualization/courseScatter')
            },
            {
                name:'courseStack',
                path:'/admin/courseStack',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/visualization/courseStack')
            },
            {
                name:'projectLine',
                path:'/admin/projectLine',
                component:()=>import(/*webpackChunkName:'teacher'*/'@/page/admin/visualization/projectLine')
            },
            {path:'',redirect:'/admin/teacherinfo'}
        ]
    },
    {

    }
]
const router = createRouter(
    {
        history: createWebHashHistory(),
        routes
    }
)

export default router
