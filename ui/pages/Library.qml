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
        ScrollBar.horizontal.policy: ScrollBar.AsNeeded

        ColumnLayout {
            width: scrollView.width
            spacing: 30

            Label {
                text: "Game Library"
                font.pixelSize: 28
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 10
            }

            Loader {
                id: noDataLoader
                active: libraryController.gamesList.length === 0
                sourceComponent: Component {
                    Label {
                        text: "No games found in the library."
                        font.pixelSize: 20
                        color: "gray"
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }

            GridView {
                id: gameGrid
                Layout.fillWidth: true
                Layout.preferredHeight: contentHeight
                Layout.leftMargin: 30
                Layout.rightMargin: 30
                cellWidth: (parent.width - Layout.leftMargin - Layout.rightMargin) / 5 - 20
                cellHeight: 320
                model: libraryController.gamesList
                visible: libraryController.gamesList.length > 0

                property int itemSpacing: 20

                delegate: Item {
                    id: cellItem
                    width: gameGrid.cellWidth - gameGrid.itemSpacing
                    height: gameGrid.cellHeight

                    Rectangle {
                        id: card
                        width: parent.width
                        height: 300
                        color: "white"
                        border.color: "gray"
                        border.width: 1
                        radius: 5
                        clip: true

                        Column {
                            id: contentColumn
                            anchors.top: parent.top
                            anchors.topMargin: 10
                            anchors.horizontalCenter: parent.horizontalCenter
                            spacing: 5
                            width: parent.width - 20

                            Image {
                                id: gameImage
                                source: Qt.resolvedUrl("../../resources/app_icons/images.jpg").toString()
                                width: 140
                                height: 140
                                fillMode: Image.PreserveAspectFit
                                anchors.horizontalCenter: parent.horizontalCenter
                            }

                            Text {
                                text: modelData.name || "Unnamed Game"
                                font.pixelSize: 14
                                horizontalAlignment: Text.AlignHCenter
                                width: parent.width
                                wrapMode: Text.WordWrap
                            }

                            Text {
                                text: "Hours: " + (modelData.total_hours || 0).toFixed(1)
                                font.pixelSize: 12
                                color: "gray"
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }

                        Column {
                            id: hoverInfo
                            anchors.top: contentColumn.bottom
                            anchors.topMargin: 10
                            anchors.horizontalCenter: parent.horizontalCenter
                            spacing: 5
                            width: parent.width - 20
                            visible: false

                            Text {
                                text: "Sessions: " + (modelData.session_count || 0)
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "First Played: " + (modelData.first_played ? modelData.first_played.slice(0, 10) : "N/A")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "Last Played: " + (modelData.last_played ? modelData.last_played.slice(0, 10) : "N/A")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "Genre: Action RPG"  // Оставил хардкод, так как этого поля нет в данных
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: {
                                card.color = "#f0f0f0"
                                hoverInfo.visible = true
                            }
                            onExited: {
                                card.color = "white"
                                hoverInfo.visible = false
                            }
                        }
                    }
                }
            }
        }
    }
}