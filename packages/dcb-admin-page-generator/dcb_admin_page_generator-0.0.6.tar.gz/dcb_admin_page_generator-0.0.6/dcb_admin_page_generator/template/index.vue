<template>
  <div class="index">
    <div class="wrap-padding-ct">
      <z_page
        title="抽奖活动管理" :query-params.sync="queryParams"
        :table-option="table_option" :data="table_list" @press="press"/>
    </div>
    <z_dialog_form
      v-if="change_edit_visible" :visible.sync="change_edit_visible"
      width="60%" v-model="change_active_info" :filed-width="'500px'" label-width="120px"
      @finish="changeFinish"
    />
<!--    <z_dialog :visible.sync="el_dialog_visible" title="修改活动信息" width="80%" @finish="updateSession">-->
<!--      <add_or_edit_step_2 ref="add_or_edit_step_2"/>-->
<!--    </z_dialog>-->
    <z_view_qr v-if="z_view_qr_visible" :visible.sync="z_view_qr_visible" :view-url="previewUrl"/>
  </div>
</template>

<script>
import Z_page from '@/components/Z/z_page';
import { zfTemplateDataDeal, zfTurnToTemplate,deepCopy } from '@/components/Z/z_funcs';
import { prepareFormData } from '@/x';
import Z_dialog_form from '@/components/Z/z_dialog_form';
import Z_view_qr from '@/components/Z/z_view_qr';
// Api writePlace

export default {
  name: 'index',
  components: { Z_view_qr, Z_dialog_form, Z_page },
  data() {
    return {
      change_edit_visible:false,
      z_view_qr_visible:false,
      queryParams: {
        fitter: [],
        pagination: {
          pageIndex: 1,
          pageSize: 10,
          total: 0,
        },
      },
      previewUrl: '',
      copyQueryParams: {},
      table_list: [{ test: '1' }],
      table_option: [],
      change_active_info: [
        { label: '活动信息', type: 'title', options: {} },
        {
          prop: 'activityName',
          label: '活动名称',
          type: 'input',
          value:  '',
          data: [],
          options: { maxlength: 15, showWordLimit: true },
          verification: 'req',
        },
        {
          prop: 'description',
          label: '活动简介',
          type: 'richText',
          value: '',
          data: [],
          options: { toolbarOptions: [['bold'], [{ color: [] }, { background: [] }]] },
          height: '200px',
          verification: 'req',
        },
        {
          prop: 'businessChannelId',
          label: '运营渠道',
          type: 'channel',
          value: '',
          data: [],
          options: { multiple: false },
          verification: 'req',
        },
        { prop: 'headImage', label: '活动头图', type: 'img', value: '', data: [], options: {}, verification: 'req' },
        {
          prop: 'backgroundColor',
          label: '活动背景颜色',
          type: 'color',
          value: '',
          data: [],
          options: {},
          verification: 'req',
        },
        {
          prop: 'rule',
          label: '活动规则',
          type: 'richText',
          value: '',
          data: [],
          options: { toolbarOptions: [['bold'], [{ color: [] }, { background: [] }]] },
          height: '200px',
          verification: 'req',
        },
        { label: '活动分享信息', type: 'title', options: { tips: '配置后用于活动被分享至微信后的分享卡片展示信息' } },
        { prop: 'shareTitle', label: '分享标题', type: 'input', value: '', data: [], options: {}, verification: 'req' },
        { prop: 'shareDesc', label: '分享描述', type: 'input', value: '', data: [], options: {}, verification: 'req' },
        { prop: 'shareImage', label: '分享略缩图', type: 'img', value: '', data: [], options: {}, verification: 'req' },
      ],
    };
  },
  async mounted() {
    await this.getDataList();
    this.copyQueryParams = deepCopy(this.queryParams);
    this.tableOperationInit();
  },
  methods: {
    press(val) {
      if (val === 'add') {
        this.$router.push({ path: 'add_or_edit', query: {} });
        // this.change_edit_visible = true

      } else if (val === 'search') {
        this.getDataList();

      } else if (val === 'reset') {
        this.queryParamsReset();
      }
    },
    tableOperationInit() {
      const tp = {}
      let target_fpt_index = this.table_option.findIndex(ele => {
        return ele.type === 'op';
      });
      this.table_option[target_fpt_index].options.tableOperationList = {
        默认: [],
      };
      console.log('this.table_option[target_fpt_index]', this.table_option[target_fpt_index]);
    },
    queryParamsReset() {
      this.queryParams = deepCopy(this.copyQueryParams);
      this.getDataList();
    },
    async getDataList() {
      let temp_q = zfTemplateDataDeal(this.queryParams.fitter);
      temp_q = { ...temp_q, ...this.queryParams.pagination };
      const data = await SOMEFUNCS_LIST(temp_q);
      this.table_list = data.list;
      this.queryParams.pagination.total = data.total;
    },


    async changeFinish() {
      // const temp_form = await prepareFormData(zfTemplateDataDeal(this.change_active_info));
      // await SOMEFUNCS(temp_form);
      // this.$message.success('修改成功');
      // this.change_edit_visible = false;
    },
    view(row) {
      this.previewUrl = row.previewUrl;
      this.z_view_qr_visible = true;
      console.log('row', row.previewUrl);
    },
    // 函数填充

  },
};
</script>

<style lang="scss" scoped>
.index {
  padding: 20px;
  background-color: rgb(240, 242, 245);
  position: relative;
  height: calc(100vh - 100px);
  overflow: auto;

  .wrap-padding-ct {
    position: relative;
    min-height: calc(100vh - 140px);
    background-color: #ffffff;
    padding: 20px;
  }
}
</style>
