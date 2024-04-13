<script setup lang="ts">
import lottie from 'lottie-web';
import { onMounted } from 'vue';
import animationJson from './jumploading3.json'


onMounted(()=>{
    let ani=lottie.loadAnimation({
            container:document.getElementById("JLanimationContainer"),
            renderer: 'svg',
            loop: false,
            autoplay: true,
            animationData: animationJson,
    });


    ani.addEventListener("complete",()=>{
         document.getElementById("JLanimationContainer")?.classList.add("container_hidden")
    })  
})
</script>


<template>
    <div  class="jlcontainer" id="jlcontainer">
        <div class="JLanimationContainer" id="JLanimationContainer">
    
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
.container_hidden{
    transform: translateY(100%);
    transition: transform 1.8s ease;
}

</style>
