<!-- 업로드 -->
% rebase('base.tpl')
<div id="tool">
    <nav class="menu">
        <a class="menu-item selected" href="#" onclick="return false">
            {{title}}
        </a>
        <a class="menu-item" href="javascript:history.back(-1);">뒤로</a>
    </nav>
</div>
<h1 class="title">
    {{title}}
</h1>
<div>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <br>
        <br>
        파일명 : <input type="text" name="data">
        <br>
        <br>
        라이선스 : <input type="text" name="lice">
        <br>
        <br>
        <button class="btn btn-primary" type="submit">업로드</button>
    </form>
</div>
<span>{{number}}MB 이하 파일만 업로드 가능하고 확장자는 jpg, png, gif, jpeg만 가능합니다.</span>