<script setup lang="ts">
import { ref } from 'vue';
import dayjs from 'dayjs'

const value2 = ref(dayjs().add(1, 'month').startOf('month'))

const currentDate = new Date();
const formattedDate = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} ${currentDate.getHours()}:${currentDate.getMinutes()}:${currentDate.getSeconds()}`;
const value1 = ref(formattedDate);
const OTtasklist =ref([])


</script>

<template>
    <div class="OTbody">
        <div  class="OTcontainer">
            <div class="OTheader">
                <div class="OTheaderBlank">
                </div>
                <el-select v-model="OTtasklist"  placeholder="Select" size="large" style="width: 340px">
                    <el-option>

                    </el-option>
                </el-select>

            </div>
            <div class="OTmainer">
                <el-descriptions title="User Info" >
                    <el-descriptions-item label="Username">kooriookami</el-descriptions-item>
                    <el-descriptions-item label="Telephone">18100000000</el-descriptions-item>
                    <el-descriptions-item label="Place">Suzhou</el-descriptions-item>
                    <el-descriptions-item label="Remarks">
                        <el-tag size="small">School</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="Address">
                        No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
                    </el-descriptions-item>
                </el-descriptions>
                <div style="height: 20px;"/>
                <div class="OTstatistics">
                    <el-col :span="10">
                        <el-statistic title="任务时间" :value="value1+'~'+value2.format('YYYY-MM-DD')">
                            
                        </el-statistic>
                    </el-col>

                    <el-col :span="10">
                        <el-statistic title="完成情况" :value="0" >
                            <template #suffix>
                                <el-popover
                                    placement="top-start"
                                    title="明细"
                                    :width="600"
                                    trigger="hover"
                                    popper-style="box-shadow: rgb(14 18 22 / 20%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px; border-radius: 15px;"
                                    >
                                    <template #reference>
                                        <p>/100</p>
                                    </template>
                                    <template #default>
                                        <p>this is content</p>
                                    </template>
                                </el-popover>
                            </template>
                        </el-statistic>
                    </el-col>

                    <el-col :span="10">
                        <el-countdown format="DD [days] HH:mm:ss" :value="value2">
                            <template #title>
                            <div style="display: inline-flex; align-items: center">
                                <el-icon style="margin-right: 4px" :size="12">
                                <Calendar />
                                </el-icon>
                                剩余时间
                            </div>
                            </template>
                        </el-countdown>
                        
                    </el-col>
                </div>
                
            </div>
            
        </div>
    </div>
</template>

<style scoped>
.OTcontainer{
    margin: 30px;
    box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.3); /* 添加一个 10px 的模糊黑色阴影 */
    background-color: #ffffff;
    padding: 20px; /* 可选：为了美观，添加一些内边距 */
    border-radius: 10px;
    display: block;
    height: 100%;
}
.OTheader{
    display: flex;
    width: 100%;
}
.OTheaderBlank{
    width: 80%;
}
.OTmainer{
    display: block;
    margin: 30px;
}
.OTstatistics{
    display: flex;
}

</style>