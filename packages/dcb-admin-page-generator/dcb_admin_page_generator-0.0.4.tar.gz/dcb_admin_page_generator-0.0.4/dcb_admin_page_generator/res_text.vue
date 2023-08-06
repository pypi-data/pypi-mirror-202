<template>
    <z_dialog_page
      title="测试" only-close
      :visible="visible"
      :query-params.sync="queryParams"
      :table-option="table_option"
      :data.sync="table_list"
      @press="press"
      @update:visible="(val)=>{ $emit('update:visible',val) }"
    />
</template>

<script>
import Z_dialog_page from '@/components/Z/z_dialog_page';
import { zfTemplateDataDeal, zfTurnToTemplate,deepCopy } from '@/components/Z/z_funcs';
import { prepareFormData } from '@/x';
import { apiImsApiPurchaseNotesPageList } from '@/generated_api';

export default {
  name: 'index',
  components: {  Z_dialog_page },
  props:{
   visible:{
      default:false,
      type:Boolean
    },
  },
  data() {
    return {
      change_edit_visible:false,
      z_view_qr_visible:false,
      queryParams: {
        fitter: [{'prop': 'adminSource', 'type': 'input', 'label': '请求来源', 'value': '', 'data': [], 'options': {}}, {'prop': 'purchaseNotesId', 'type': 'input', 'label': '购买须知模板ID', 'value': '', 'data': [], 'options': {}}, {'prop': 'refUserGroupId', 'type': 'input', 'label': '运营渠道ID', 'value': '', 'data': [], 'options': {}}, {'prop': 'storeId', 'type': 'input', 'label': '店铺ID', 'value': '', 'data': [], 'options': {}}, {'prop': 'templateName', 'type': 'input', 'label': '模板名称', 'value': '', 'data': [], 'options': {}}, {'prop': 'templateType', 'type': 'select', 'label': '购买须知模板', 'value': '', 'data': [{'key': '0', 'value': '平台模板 '}, {'key': '1', 'value': '门店模板'}], 'options': {}}],
        pagination: {
          pageIndex: 1,
          pageSize: 10,
          total: 0,
        },
      },
      previewUrl: '',
      copyQueryParams: {},
      table_list: [],
      table_option: [{'prop': 'merchantName', 'type': 'str', 'label': '所属商户名称', 'value': '', 'data': [], 'options': {}}, {'prop': 'purchaseNotesId', 'type': 'str', 'label': '购买须知ID', 'value': '', 'data': [], 'options': {}}, {'prop': 'refMerchantId', 'type': 'str', 'label': '所属商户ID', 'value': '', 'data': [], 'options': {}}, {'prop': 'refUserGroupId', 'type': 'str', 'label': '运营渠道ID', 'value': '', 'data': [], 'options': {}}, {'prop': 'refUserGroupName', 'type': 'str', 'label': '运营渠道名称', 'value': '', 'data': [], 'options': {}}],
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
      if (target_fpt_index !== -1){
       this.table_option[target_fpt_index].options.tableOperationList = {
        默认: [],
        };
      }
      console.log('this.table_option[target_fpt_index]', this.table_option[target_fpt_index]);
    },
    queryParamsReset() {
      this.queryParams = deepCopy(this.copyQueryParams);
      this.getDataList();
    },
    async getDataList() {
      let temp_q = zfTemplateDataDeal(this.queryParams.fitter);
      temp_q = { ...temp_q, ...this.queryParams.pagination };
      const data = await apiImsApiPurchaseNotesPageList(temp_q);
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

</style>
