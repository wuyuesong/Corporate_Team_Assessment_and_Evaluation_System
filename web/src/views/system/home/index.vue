<template>
	<div style="display: block; text-align: center; justify-items: center; ">
		<div style="text-align: center;font-size: 40px;font-weight: bold; margin: 40px;">WELCOME</div>
    	<div class="text-3xl" ref="hero" style="line-height: 1.7;">
    	</div>
	</div>



</template>

<script setup lang="ts">
import { ref ,onMounted, nextTick} from 'vue';
import TypeIt from 'typeit';

const hero = ref();

const homedialogVisible= ref(false);
onMounted(() => {

	new TypeIt(hero.value, {
  speed: 50,
  startDelay: 900,
})
  .type("欢迎使用我们的系统！", { delay: 100 })
  .move(null, { to: "START", instant: true, delay: 300 })
  .type("您好？", { delay: 200 })
  .move(0, { delay: 200 })
  .delete(1,{ delay: 200 })
  .type("！", { delay: 225 })
  .pause(200)
  .move(null, { to: "END" })
  .break()
  .type("我们一直在努力为您提供最好的体验。", { delay: 100 })
  .break() // 插入一个换行符
  .type("如果您有bug，", { delay: 100 })
  .break()
  .type("请随时向我们反馈。", { delay: 100 })
  .move(-11, { delay: 200 })
  .delete(3,{ delay: 200 })
  .type("任何问题建议",{speed:50})
  .move(-2, { delay: 200 })
  .type("或",{ delay: 100 })
  .move(null, { to: "END" })
  .type(' please <span class="place">contact us</span>', { delay: 400 })
  .delete(".place", { delay: 800, instant: true })
  .type('<span><strong class="font-semibold">contact us.</strong></span>', {
    speed: 100,
  })
  .move(-30,{ delay: 10 , instant: true})
  .delete(5,{ delay: 50 })
  .type('<em id="advice" class="text-slate-500 hover:text-teal-600 cursor-pointer underline">问题或建议</em>', {
    speed: 100,
  })
  .move(null, { to: "END" })
  .go()
})



</script>

<style scoped>

</style>
