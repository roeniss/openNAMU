let pasteUploadSwitch = false;
function togglePasteUploaderSwtich() {
  pasteUploadSwitch = !pasteUploadSwitch;
  if (pasteUploadSwitch) {
    const textarea = document.querySelector("textarea");
    if (textarea) textarea.addEventListener("paste", pasteListener);
    alert("이미지 복붙 업로드 활성화");
  } else {
    const textarea = document.querySelector("textarea");
    if (textarea) textarea.removeEventListener("paste", pasteListener);
    alert("이미지 복붙 업로드 비활성화");
  }
}

function pasteListener(e) {
  // find file
  if (e.clipboardData && e.clipboardData.items) {
    const items = e.clipboardData.items;
    let haveImageInClipboard = false;
    const formData = new FormData();
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf("image") !== -1) {
        const file = items[i].getAsFile();
        const customName = prompt("파일 이름을 설정해주세요. (확장자는 생략)");
        if (!customName) return alert("취소되었습니다.")
        const customFile = new File([file], customName + ".png", { type: file.type });
        formData.append("f_data[]", customFile);
        haveImageInClipboard = true;
        e.preventDefault();
        break;
      }
    }
    if (!haveImageInClipboard) return;

    // send to server
    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((res) => {
        if (res.status === 200 || res.status === 201) {
          const url = res.url;
          alert(
            `이미지 복붙 업로드 성공. 아래 텍스트로 본문에 삽입할 수 있습니다.
[[${decodeURIComponent(url.replace(/.*\/w\/file/, "file"))}]]`
          );
        } else {
          console.error("[ERROR] PasteUpload Fail :", res.statusText);
          alert("이미지 복붙 업로드에 실패했습니다. 파일명 중복일 수 있습니다.");
        }
      })
      .catch((err) => {
        console.error("[ERROR] PasteUpload Fail :", JSON.stringify(err), err);
        alert("이미지 복붙 업로드에 실패했습니다. 파일명 중복일 수 있습니다.");
      });
  }
}
