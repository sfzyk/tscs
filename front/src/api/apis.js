import axios from './http'
import qs from 'qs'
import { isNull } from 'util';

const GET = (uri, json) => axios.get(uri, json)
const POST = (uri, json) => axios.post(uri, json)

const host = 'http://59.110.224.120'

const api = {
  register: (year, email, password, name, telephone, id, major, department, birthdate) => POST(`${host}/student/register/`, qs.stringify({
    'email': email,
    'password': password,
    'year': year,
    'name': name,
    'telephone': telephone,
    'major': major,
    'department': department,
    'id': id,
    'birth_date': birthdate,
  })),
  login: (email, password) => POST(`${host}/student/login/`, qs.stringify({
    'email': email,
    'password': password
  })),
  logout: () => POST(`${host}/student/logout/`, qs.stringify({})),
  adminlogin: (email, password) => POST(`${host}/administrator/login/`, qs.stringify({
    'email': email,
    'password': password
  })),
  admin_logout: () => POST(`${host}/administrator/logout/`, qs.stringify({})),
  expertlogin: (email, password) => POST(`${host}/expert/login/`, qs.stringify({
    'email': email,
    'password': password
  })),
  expert_logout: () => POST(`${host}/expert/logout/`, qs.stringify({})),
  stage_application: (cooperatorinfo, email, fullname, telephone, address, innovation, keywords, category, descriptions, education_background, type, type_info,contest_id) => POST(`${host}/project/project_stage/`, qs.stringify({
    'full_name': fullname,
    'telephone': telephone,
    'cooperator_info': cooperatorinfo,
    'address': address,
    'innovation': innovation,
    'keywords': keywords,
    'category': category,
    'descriptions': descriptions,
    'email': email,
    'type': type,
    'type_info': type_info,
    'education_background': education_background,
    'contest_id':contest_id,
  })),
  modify_application: (id, info) => POST(`${host}/project/project_modify/`, qs.stringify({
    'info': info,
    'id': id
  })),
  submit_application: (id) => POST(`${host}/project/project_submit/`, qs.stringify({
    'proj_id': id
  })),
  delete_application: (id) => POST(`${host}/project/project_delete/`, qs.stringify({
    "proj_id": id
  })),
  get_user_info: () => GET(`${host}/student/user_info/`, qs.stringify({})),
  /*
  modify_user_info:(year, email, name, telephone , major, department, birth_date)=> PUT(`${host}/student/user_info`, qs.stringify({
	  'year': year,
	  'email': email,
	  'name': name,
	  'telephone': telephone,
	  'major': major,
	  'department': department,
	  'birth_date': birth_date
  })),*/
  modify_user_info: (info) => POST(`${host}/student/user_info/`, qs.stringify(info)),
  student_get_projects: (index, pagesize, info) => POST(`${host}/student/projects/${index}/${pagesize}/`, qs.stringify(info)),
  student_get_project: (proj_id) => GET(`${host}/student/project_info/${proj_id}/`, qs.stringify({})),
  administrator_get_project: (proj_id) => GET(`${host}/administrator/project_info/${proj_id}/`, qs.stringify({})),
  admin_get_projects: (index, pagesize, info) => POST(`${host}/administrator/projects/${index}/${pagesize}/`, qs.stringify(info)),
  /*
  field : str
  order : 1 asc 2 desc 
  search :{
  }
  search 可选项：["innovation", "descriptions", "email", "telephone", "name", "keywords"]
                 ['state', 'contest_id', 'expire', 'education_background', "category", "type"]
  */
  admin_get_projects_by_contest: (index, pagesize, info, contest_id) => POST(`${host}/administrator/projects/${index}/${pagesize}/${contest_id}/`, qs.stringify(info)),
  review_project: (proj_id) => POST(`${host}/administrator/review_project/`, qs.stringify({ "proj_id": proj_id })),
  revert_project: (proj_id) => GET(`${host}/administrator/revert_project/${proj_id}/`, qs.stringify({})),
  /*
  info :
  ["name", "descriptions", "expire_date", "checkin_expire_date"]
  ['state']
  */
  student_get_contest:(index, pagesize, info) => POST(`${host}/student/contests/${index}/${pagesize}/`, qs.stringify(info)), 
  student_get_contest_info: (contest_id) => GET(`${host}/student/contest_info/${contest_id}/`, qs.stringify({})),
  
  get_contest: (index, pagesize, info) => POST(`${host}/contest/contest/${index}/${pagesize}/`, qs.stringify(info)),
  get_contest_info: (contest_id) => GET(`${host}/contest/info/${contest_id}/`, qs.stringify({})),
  add_contest: (name, descriptions, expire_date, stop_date) => POST(`${host}/contest/`, qs.stringify({
    "name": name,
    "descriptions": descriptions,
    "expire_date": expire_date,
    "stop_date": stop_date,
  })),

  /*
  options :
  checkin_expire_date
  expire_date
  descriptions
  name
  */
  modify_contest: (info) => POST(`${host}/contest/modify/`, qs.stringify(
    info
  )),
  delete_contest: (contest_id) => POST(`${host}/contest/delete/`, qs.stringify({
    "contest_id": contest_id
  })),

  publish_contest: (contest_id) => POST(`${host}/contest/publish/`, qs.stringify({
    "contest_id": contest_id
  })),
  recheck_contest: (contest_id) => POST(`${host}/contest/recheck/`, qs.stringify({
	"contest_id": contest_id
  })),
  stop_checkin_contest: (contest_id) => POST(`${host}/contest/stop/`, qs.stringify({
    "contest_id": contest_id
  })),
  finish_check_contest: (contest_id) => POST(`${host}/contest/finish/`, qs.stringify({
    "contest_id": contest_id
  })),
  add_to_project: (expert_id, project_id) => POST(`${host}/expert/add_to_project/`, qs.stringify({
    "expert_id": expert_id,
    "proj_id": project_id
  })),
  delete_from_project: (relation_id) => POST(`${host}/expert/delete/`, qs.stringify({
    "expert_project_id": relation_id
  })),

  delete_image: (img_id) => POST(`${host}/resources/image_delete/`, qs.stringify({
    "img_id": img_id
  })),
  get_project_image: (proj_id) => GET(`${host}/resources/image_name/${proj_id}/`, qs.stringify({})),
  get_project_video: (proj_id) => GET(`${host}/resources/video_name/${proj_id}/`, qs.stringify({})),
  get_project_document: (proj_id) => GET(`${host}/resources/document_name/${proj_id}/`, qs.stringify({})),

  add_image(image, proj_id) {
    var fd = new FormData();
    fd.append("image", image);
    fd.append("proj_id", proj_id);
    return POST(`${host}/resources/image/`, fd)
  },
  add_video(video, proj_id) {
    var fd = new FormData();
    fd.append("video", video);
    fd.append("proj_id", proj_id);
    return POST(`${host}/resources/video/`, fd)
  },
  add_document(document, proj_id) {
    var fd = new FormData();
    fd.append("document", document);
    fd.append("proj_id", proj_id);
    return POST(`${host}/resources/document/`, fd)
  },
  download_image: (img_id) => GET(`${host}/resources/image/${img_id}`),
  delete_video: (video_id) => POST(`${host}/resources/video_delete/`, qs.stringify({
    "video_id": video_id
  })),
  download_video: (video_id) => GET(`${host}/resources/video/${video_id}/`, qs.stringify({})),
  delete_document: (document_id) => POST(`${host}/resources/document_delete/`, qs.stringify({
    "document_id": document_id
  })),
  download_document: (document_id) => GET(`${host}/resources/document/${document_id}/`, qs.stringify({})),

  example_expertinfo() {
    // let aTag = document.createElement("a");
    // let blob = new Blob([`${host}/administrator/example_info/`]); // 这个content是下载的文件内容，自己修改
    // aTag.download = "评委列表模板.xlsx"; // 下载的文件名
    // aTag.href = URL.createObjectURL(blob);
    // aTag.click();
    // URL.revokeObjectURL(blob);
    window.open(`${host}/administrator/example_info/`)
  },
  //=> GET(`${host}/administrator/example_info/`, qs.stringify({})),
  /*
  options
  field str
  order 1a 2d
  search json
  {
    "name": "wang"
  }
     ["name", "email", "field", "college", 'telephone']
     ['state']
  */
  get_experts: (index, pagesize, info) => POST(`${host}/expert/experts/${index}/${pagesize}/`, qs.stringify(info)),
  experts_contests: (index, pagesize, info, contest_id) => POST(`${host}/expert/experts_contests/${index}/${pagesize}/${contest_id}/`, qs.stringify(info)),
  expert_info: ()=> GET(`${host}/expert/user_info/`, qs.stringify({})),
  student_zip_file(proj_id) {
    // let aTag = document.createElement("a");
    // let blob = new Blob([`http://59.110.224.120/resources/student_zip_file/${proj_id}`]); // 这个content是下载的个content是下载的文件内容，自己修改
    // aTag.download = proj_name + '.zip'; // 下载的文件名
    // aTag.href = URL.createObjectURL(blob);
    // aTag.click();
    // URL.revokeObjectURL(blob);
    window.open(`http://59.110.224.120/resources/student_zip_file/${proj_id}`)
  },
  fileview(type, id) {
    window.open(
      `http://59.110.224.120/resources/${type}/${id}`
    );
  },
  /*
  info :
  必有 field , email 
  可有 name,telephone,college
  */
  load_expert: (info) => POST(`${host}/administrator/load_expert/`, qs.stringify(info)),
  load_experts(file) {
    var fd = new FormData();
    fd.append("file", file);
    return POST(`${host}/administrator/load_experts/`, fd)
  },
  delete_expert: (expert_id) => POST(`${host}/administrator/delete_expert/`, qs.stringify({ "expert_id": expert_id })),
  delete_all_expert: () => POST(`${host}/administrator/delete_all_expert/`, qs.stringify({})),
  /*为一个项目自动分配专家*/
  auto_dispatch: (contest_id) => GET(`${host}/expert/auto_dispatch/${contest_id}/`,qs.stringify({})),
  /*清空一个项目目前的分配*/
  reset_dispatch: (contest_id) => GET(`${host}/expert/resest_dispatch/${contest_id}/`,qs.stringify({})),
  /* 手动给竞赛分配专家 */
  manual_dispatch: (contest_id, ids)=> POST(`${host}/expert/manual_dispatch/`, qs.stringify({
      "contest_id":contest_id,
      "ids":ids
    }
  )),
  /* 获取邀请进度*/
   dispatch_percent: (contest_id) => GET(`${host}/expert/dispath_percent/${contest_id}/`, qs.stringify({})),
  /*
  发送邀请邮件 
  */
  send_email: (contest_id) => GET(`${host}/contest/finish_dispatch/${contest_id}/`, qs.stringify({})),
  /*
  必有 : expert_id
  可有 ：['name', 'password', 'college', 'telephone']
  */
  modify_expert: (info) => POST(`${host}/administrator/modify_expert/`, qs.stringify(info)),

  expert_login: (password, email) => POST(`${host}/expert/login/`, qs.stringify({
    "email": email,
    "password": password
  })),
  /* 专家获取项目列表 */
  expert_get_projects: (index, pagesize, info)=> POST(`${host}/expert/projects/${index}/${pagesize}/`, qs.stringify(info)),
  /* 装甲获取项目 */
  expert_get_project: (proj_id) => GET(`${host}/expert/project/${proj_id}/`, qs.stringify({})),
  /*
  可选:['name', 'password', 'college', 'telephone']stringfy
  */
  expert_modifty_info: (info) => POST(`${host}/expert/modifty/`, qs.stringify(info)),
  expert_zip_file()
  {
    window.open(
      `http://59.110.224.120/expert/zip_file/`
    );
  },
  admin_zip_file(id)
  {
    window.open(
      `http://59.110.224.120/administrator/zip_file/${id}`
    );
  },
  /*
  options :
  auto_dispath
  */
  modify_config: (info) => POST(`${host}/administrator/config/`, qs.stringify(info)),
  add_notice(attach,title,content){
    var fd = new FormData();
    if (!isNull(attach)){
      fd.append("attach", attach);
    }
    fd.append("title", title);
    fd.append("content",content);
    return POST(`${host}/notice/add_notice/`, fd);
  },
  get_notice:(notice_id)=>POST(`${host}/notice/get_notice/`,qs.stringify({
    "notice_id":notice_id
  })),
  get_attach(notice_id)
  {
    window.open(
      `${host}/notice/get_attach/?notice_id=${notice_id}`
    );
  },
  // =>POST(`${host}/notice/get_attach/`,qs.stringify({
  //   "notice_id":notice_id
  // })),
  delete_notice:(notice_id)=>POST(`${host}/notice/delete_attach/`,qs.stringify({
    "notice_id":notice_id
  })),
  get_notice_list:()=>POST(`${host}/notice/get_list/`),
  commit_comment:(project_id)=>POST(`${host}/comment/comment_submit/`,qs.stringify({
    "project_id":project_id
  })),
  stage_comment:(project_id,comment,score)=>POST(`${host}/comment/comment_stage/`,qs.stringify({
    "project_id":project_id,
    "comment":comment,
    "score":score
	})),
  /* 终审名单api */
  enter_final : (contest_id,ids) => POST(`${host}/contest/enter_final/`,qs.stringify({
	"contest_id" : contest_id,
	"ids": ids
  })),
  stage_final: (contest_id,ids) => POST(`${host}/contest/stage_final/`,qs.stringify({
	"contest_id" : contest_id,
	"ids": ids
  })),
  get_final: (contest_id) => POST(`${host}/contest/get_final/`, qs.stringify({
    "contest_id":contest_id
  })),
  
  get_expert_project_comment:(project_id)=>POST(`${host}/comment/project_comment/`,qs.stringify({
    "project_id":project_id
  })),

  invitation_info: (uuid)=>POST (`${host}/expert/invitation/info/`, qs.stringify({
    "uni_link": uuid
  })),
  
 /*
 必选：
 uni_link 
 join
 可选:
 password
 */
  invitation_reset: (info)=>POST (`${host}/expert/invitation/rest/`, qs.stringify(info)),
  
  /*
  系统参数
  */
  get_info: ()=> GET(`${host}/administrator/sys_info/`, qs.stringify({})),
  /*
  可选参数 
  num_proj
  expert_per_proj
  */
  modifty: (info)=> POST(`${host}/administrator/modify_sys_info/`, qs.stringify(info)),
  /*
  */
  admin_commmet: (proj_id) => GET(`${host}/administrator/comment/${proj_id}/`, qs.stringify({})),
}
export default api
