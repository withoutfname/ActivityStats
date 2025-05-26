SimpleEditDialog {
    id: editDialog
    title: "Edit Game Metadata"
    standardButtons: Dialog.Close  // Кнопка закрытия

    width: 200
    height: 100

    Label {
        anchors.centerIn: parent
        text: "Привет"
        font.pixelSize: 16
    }
}