// ui/main.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "ActivityStats"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10

        Label {
            text: "Выберите игру"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        ComboBox {
            Layout.fillWidth: true
            model: ["Пока нет данных"] // Заглушка, позже заменим
        }
    }
}