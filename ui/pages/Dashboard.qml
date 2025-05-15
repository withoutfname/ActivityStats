import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        Label {
            text: "Your Gaming Stats"
            font.pixelSize: 28
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Total Playtime: " + controller.totalPlaytime.toFixed(1) + " hours"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 10

            Label {
                text: "Top Games"
                font.pixelSize: 18
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            Repeater {
                model: controller.topGames
                Label {
                    text: modelData[0] + ": " + modelData[1].toFixed(1) + " hours"
                    font.pixelSize: 16
                    Layout.alignment: Qt.AlignHCenter
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 10

            Label {
                text: "Select Period (WIP)"
                font.pixelSize: 18
                Layout.alignment: Qt.AlignHCenter
            }

            Slider {
                from: 1
                to: 30
                value: 1
                Layout.fillWidth: true
                enabled: false
            }
        }

        Rectangle {
            Layout.preferredWidth: 200
            Layout.preferredHeight: 200
            Layout.alignment: Qt.AlignHCenter
            color: "#ddd"
            radius: 100
            Label {
                anchors.centerIn: parent
                text: "Pie Chart (WIP)"
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }
}