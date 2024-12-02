<script setup lang="ts">
import lottie from 'lottie-web';
import { onMounted, ref } from 'vue';
import animationJson from './jumploading3.json'

const JLC=ref()
onMounted(()=>{
    let ani=lottie.loadAnimation({
            container:document.getElementById("JLanimationContainer"),
            renderer: 'svg',
            loop: false,
            autoplay: true,
            animationData: animationJson,
    });


    ani.addEventListener("complete",()=>{
        document.getElementById("JLanimationContainer")?.classList.add("container_visible")
    })  
    // 添加双击事件监听器
    JLC.value.addEventListener("dblclick", function() {
        // 将动画跳转到最后一帧
        ani.goToAndPlay(8500, false);
    });


})
</script>


<template>
    <div  class="jlcontainer" id="jlcontainer">
        <div class="JLanimationContainer" ref="JLC" id="JLanimationContainer">
    
        </div>
    </div>
</template>
<style>
#jlcontainer{

}
#JLanimationContainer{
    position: absolute;
    display:flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background-color: #dedede;
    z-index: 100;
    
}
/* .container_hidden{
    transform: translateY(100%);
    transition: transform 1.3s ease;
} */
.container_visible{
    max-height: 0;
}

</style>
