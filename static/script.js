function imgSize(_item) {
    var newWidth = _item.clientWidth / (_item.clientHeight / 600);
    var newHeight = 600;
    _item.width = newWidth;
    _item.height = newHeight;
}