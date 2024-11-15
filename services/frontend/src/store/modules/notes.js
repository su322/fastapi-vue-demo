// 导入 axios 库，用于发送 HTTP 请求
import axios from 'axios';

// 定义状态
const state = {
  // 存储所有笔记的数组
  notes: null,
  // 存储当前选中笔记的对象
  note: null
};

// 定义获取器
const getters = {
  // 获取所有笔记
  stateNotes: state => state.notes,
  // 获取当前笔记
  stateNote: state => state.note,
};

// 定义动作
const actions = {
  // 创建新笔记
  async createNote({ dispatch }, note) {
    // 发送 POST 请求到 notes 接口
    await axios.post('notes', note);
    // 重新获取所有笔记
    await dispatch('getNotes');
  },
  // 获取所有笔记
  async getNotes({ commit }) {
    // 发送 GET 请求到 notes 接口
    let { data } = await axios.get('notes');
    // 将获取到的笔记数据提交到 mutations 中更新状态
    commit('setNotes', data);
  },
  // 查看单个笔记
  async viewNote({ commit }, id) {
    // 发送 GET 请求到 note/id 接口
    let { data } = await axios.get(`note/${id}`);
    // 将获取到的笔记数据提交到 mutations 中更新状态
    commit('setNote', data);
  },
  // 更新笔记
  // eslint-disable-next-line no-empty-pattern
  async updateNote({}, note) {
    // 发送 PATCH 请求到 note/id 接口
    await axios.patch(`note/${note.id}`, note.form);
  },
  // 删除笔记
  // eslint-disable-next-line no-empty-pattern
  async deleteNote({}, id) {
    // 发送 DELETE 请求到 note/id 接口
    await axios.delete(`note/${id}`);
  }
};

// 定义突变
const mutations = {
  // 设置所有笔记
  setNotes(state, notes) {
    state.notes = notes;
  },
  // 设置当前笔记
  setNote(state, note) {
    state.note = note;
  },
};

// 导出 Vuex 模块
export default {
  state,
  getters,
  actions,
  mutations
};
