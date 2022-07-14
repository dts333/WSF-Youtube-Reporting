function get_all_ids_from_yt_studio_search() {
    l = [];
    for (let x of document.getElementsByClassName("style-scope ytcp-video-list-cell-video")) {
        l.push(x);
    }
    ar = [];
    for (let v of l.filter(x => {return x.id == 'video-title'}).slice(5)) {
        ar.push(v.href.split('/').at(-2))
    }
    return ar;
}