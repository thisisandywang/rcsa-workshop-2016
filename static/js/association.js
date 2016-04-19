function initialSetup ( elements ) {
    for( i = 0; i < elements.length; i++){
        element = elements[i]
        if(element.id.localeCompare('structure-popup') != 0){
            element.style.display = 'none'
        }
    }
}

function replaceView ( elements, name ) {
    for( i = 0; i < elements.length; i++){
        element = elements[i]
        if(element.id.substring(0, element.id.length-5).localeCompare(name.substring(0, name.length-5)) != 0){
            element.style.display = 'none'
        }
        else{
            element.style.display = 'block'
        }
    }
}

function hide ( titles, popups ) {
    structureTitle = document.getElementById('structure-title')
    structureTitle.onclick = function(){
        replaceView(popups, structureTitle.id)
    }
    
    tiersTitle = document.getElementById('tiers-title')
    tiersTitle.onclick = function(){
        replaceView(popups, tiersTitle.id)
    }
    housesTitle = document.getElementById('houses-title')
    housesTitle.onclick = function(){
        replaceView(popups, housesTitle.id)
    }
    profileTitle = document.getElementById('profile-title')
    profileTitle.onclick = function(){
        replaceView(popups, profileTitle.id)
    }
    communicationsTitle = document.getElementById('communications-title')
    communicationsTitle.onclick = function(){
        replaceView(popups, communicationsTitle.id)
    }
    rohpTitle = document.getElementById('rohp-title')
    rohpTitle.onclick = function(){
        replaceView(popups, rohpTitle.id)
    }
    tedxTitle = document.getElementById('tedx-title')
    tedxTitle.onclick = function(){
        replaceView(popups, tedxTitle.id)
    }
    scholarconnectTitle = document.getElementById('scholarconnect-title')
    scholarconnectTitle.onclick = function(){
        replaceView(popups, scholarconnectTitle.id)
    }

    committeesTitle = document.getElementById('committees-title')
    committeesTitle.onclick = function(){
        replaceView(popups, committeesTitle.id)
    }
    
}

popups = document.querySelectorAll("[id$='-popup']")
initialSetup(popups)
hide(document.querySelectorAll("[id$='-title']"), document.querySelectorAll("[id$='-popup']"))
		
