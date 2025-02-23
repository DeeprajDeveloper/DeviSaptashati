let initVerseRadioBtn = document.querySelectorAll("[id^='verse-']");
let chapterVerseRadioBtn = document.querySelectorAll("[id^='chapter-']");
let concludingVerseRadioBtn = document.querySelectorAll("[id^='exit-']");

let initVerseRadioBtnList = [...initVerseRadioBtn];
let chapterVerseRadioBtnList = [...chapterVerseRadioBtn];
let concludingVerseRadioBtnList = [...concludingVerseRadioBtn];
let verseName;

initVerseRadioBtnList.forEach(node => {
    node.addEventListener('click', () => {
        verseName = node.value;
        node.parentElement.className = "radio-selected";
        console.log(
            `${generateDateTime(new Date())} Sending Function Call to - fetchVerse(${verseName}, introduction)`
        );
        fetchVerse(verseName, "introduction");
    });
});

chapterVerseRadioBtnList.forEach((node) => {
    node.addEventListener("click", () => {
        verseName = node.value;
        node.parentElement.className = "radio-selected";
        console.log(
            `${generateDateTime(new Date())} Sending Function Call to - fetchVerse(${verseName}, chapters)`
        );
        fetchVerse(verseName, "chapters");
    });
});

concludingVerseRadioBtnList.forEach((node) => {
    node.addEventListener("click", () => {
        verseName = node.value;
        node.parentElement.className = "radio-selected";
        console.log(
            `${generateDateTime(new Date())} Sending Function Call to - fetchVerse(${verseName}, conclusion)`
        );
        fetchVerse(verseName, "conclusion");
    });
});


async function fetchVerse(verseName, verseType) {
    
    console.info(`${generateDateTime(new Date())} Call received for '${verseName}'`);
    
    var divMainContainer = document.getElementById("verses-container");

    Array.from(divMainContainer.children).forEach((child) => {
        divMainContainer.removeChild(child);
    });

    try {
        console.log(`${generateDateTime(new Date())} API call send to Application`);
        const response = await fetch("/api/search/versesByName", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                verseName: verseName,
                lang: 'hn'
            }),
        });

        var jsonDataResponse = await response.json();
        var container = document.getElementById("verses-container");
        
        console.log(`${generateDateTime(new Date())} API response received from Application`);
        
        jsonDataResponse["dataExtract"].forEach((item) => {
            var divShlokaMainContainer = document.createElement('div');
            var pVerseSanskrit = document.createElement("p");
            var pVerseLatin = document.createElement("p");
            var pVerseNo = document.createElement("p");

            pVerseSanskrit.innerHTML = `<hindi>${item["verseInformation"]["shlokaDevanagari"]}</hindi>`;
            pVerseLatin.innerHTML = item["verseInformation"]["shlokaIAST"];
            
            if (item["verseInformation"]["verseNo"] !== "" && item["verseInformation"]["verseNo"] !== null) {
                pVerseNo.innerHTML = `VerseNo: ${item["verseInformation"]["verseNo"]}`;
                pVerseNo.id = "shloka-verse-no";
            }

            pVerseLatin.className = "latin-text";
            pVerseSanskrit.id = "shloka-container-hindi";
            pVerseLatin.id = "shloka-container-latin";

            divShlokaMainContainer.id = "shloka-container";

            divShlokaMainContainer.append(pVerseSanskrit);
            divShlokaMainContainer.append(pVerseNo);
            divShlokaMainContainer.append(pVerseLatin);

            container.append(divShlokaMainContainer);
        });

        // container.appendChild(divMeaningMainContainer);
        console.log(`${generateDateTime(new Date())} Populating HTML page`);
    } catch (error) {
        console.error("Error fetching verse:", error);
        var container = document.getElementById("verses-container");
        var errorMessage =
            "Something went wrong while fetching information from the database.\nPlease contact the developer to report this issue. See below for details.";
        container.innerText = `${errorMessage} \n\nERROR MESSAGE\n${error} \n\nREQUEST\nVerseName:${verseName}, Endpoint: /api/search/versesByName`;
        container.classList.add('error');
    }
}


function generateDateTime(date) {
    // return date.toISOString().replace("T", " ").substring(0, 19);
    const p = new Intl.DateTimeFormat("en", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
    })
        .formatToParts(date)
        .reduce((acc, part) => {
            acc[part.type] = part.value;
            return acc;
        }, {});

    return `${p.year}-${p.month}-${p.day} ${p.hour}:${p.minute}:${p.second}`;
}

