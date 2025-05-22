import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    Component.onCompleted: libraryController.fetchGames()

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        ColumnLayout {
            width: parent.width - 40  // Учитываем общие отступы
            anchors.left: parent.left
            anchors.leftMargin: 20
            anchors.rightMargin: 20


            Label {
                text: "Game Library"
                font.pixelSize: 28
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            GridView {
                id: gameGrid
                Layout.fillWidth: true
                Layout.preferredHeight: contentHeight
                cellWidth: 300
                cellHeight: 300

                model: libraryController.gamesList


                delegate: Rectangle {
                    width: 250
                    height: 250
                    color: "white"
                    border.color: "gray"
                    border.width: 1

                    Text {
                        text: modelData.name || "Unnamed Game"
                        font.pixelSize: 16
                        anchors.centerIn: parent
                    }
                }
            }
        }
    }
}