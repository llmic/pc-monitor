// 验证脚本 - 在浏览器控制台运行此脚本
function verifyFix() {
    console.log('=== PC Monitor Verification ===');
    
    // 检查元素是否存在
    var currentTimeDisplay = document.getElementById('currentTimeDisplay');
    var statusLight = document.getElementById('statusLight');
    var statusText = document.getElementById('statusText');
    
    console.log('1. Element Check:');
    console.log('   currentTimeDisplay:', currentTimeDisplay ? 'FOUND' : 'NOT FOUND');
    console.log('   statusLight:', statusLight ? 'FOUND' : 'NOT FOUND');
    console.log('   statusText:', statusText ? 'FOUND' : 'NOT FOUND');
    
    // 检查状态灯类
    console.log('\n2. Status Light Classes:');
    if (statusLight) {
        console.log('   Class:', statusLight.className);
        console.log('   Has status-normal:', statusLight.classList.contains('status-normal'));
        console.log('   Has status-warning:', statusLight.classList.contains('status-warning'));
        console.log('   Has status-danger:', statusLight.classList.contains('status-danger'));
    }
    
    // 检查状态文本
    console.log('\n3. Status Text:');
    if (statusText) {
        console.log('   Content:', statusText.innerHTML);
    }
    
    // 检查时间显示
    console.log('\n4. Current Time Display:');
    if (currentTimeDisplay) {
        console.log('   Current value:', currentTimeDisplay.textContent);
        
        // 验证时间格式
        var timePattern = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;
        console.log('   Valid format:', timePattern.test(currentTimeDisplay.textContent));
    }
    
    // 测试时间更新
    console.log('\n5. Testing Time Update (wait 2 seconds)...');
    var initialTime = currentTimeDisplay ? currentTimeDisplay.textContent : 'N/A';
    
    setTimeout(function() {
        var newTime = currentTimeDisplay ? currentTimeDisplay.textContent : 'N/A';
        console.log('   Initial time:', initialTime);
        console.log('   Updated time:', newTime);
        console.log('   Time updated:', initialTime !== newTime);
        
        console.log('\n=== Verification Complete ===');
        console.log('If all checks pass, the fix is working correctly!');
    }, 2000);
}

// 自动运行验证
verifyFix();