import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt.labs.platform 1.1 as Platform

Item {
    Component.onCompleted: {
        console.log("Fetching games...")
        libraryController.fetchGames()
        console.log("Games fetched:", JSON.stringify(libraryController.gamesList))
    }

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
                cellHeight: 360
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
                        height: 340
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
                                source: "resources/app_icons/2_icon.jpg"
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
                                text: "First Played: " + (modelData.first_played ? Qt.formatDate(new Date(modelData.first_played), "dd-MM-yyyy") : "N/A")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "Last Played: " + (modelData.last_played ? Qt.formatDate(new Date(modelData.last_played), "dd-MM-yyyy") : "N/A")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "Genre: " + (modelData.genre || "Unknown")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "Year: " + (modelData.year || "N/A")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }

                        RowLayout {
                            id: buttonRow
                            anchors.right: parent.right
                            anchors.bottom: parent.bottom
                            anchors.rightMargin: 10
                            anchors.bottomMargin: 10
                            spacing: 5
                            visible: true

                            Button {
                                id: autoButton
                                implicitWidth: 40
                                implicitHeight: 40
                                background: Rectangle {
                                    color: "transparent"
                                    radius: 5
                                }
                                Image {
                                    source: Qt.resolvedUrl("../../resources/images/auto_parse_icon.png").toString()
                                    anchors.centerIn: parent
                                    width: 24
                                    height: 24
                                    fillMode: Image.PreserveAspectFit
                                }
                                onClicked: {
                                    console.log("Auto parse clicked for", modelData.name)
                                }
                            }

                            Button {
                                id: manualButton
                                implicitWidth: 40
                                implicitHeight: 40
                                background: Rectangle {
                                    color: "transparent"
                                    radius: 5
                                }
                                Image {
                                    source: Qt.resolvedUrl("../../resources/images/manual_icon.png").toString()
                                    anchors.centerIn: parent
                                    width: 24
                                    height: 24
                                    fillMode: Image.PreserveAspectFit
                                }
                                onClicked: {
                                    console.log("Manual parse clicked for", modelData.name)
                                    editDialog.currentGame = modelData
                                    editDialog.open()
                                }
                            }
                        }

                        MouseArea {
                            anchors.fill: hoverInfo
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

    Dialog {
        id: editDialog
        title: "Edit Game Metadata"
        standardButtons: Dialog.Close
        width: 800
        height: 800
        anchors.centerIn: parent

        property var currentGame: ({})

        onOpened: {
            if (currentGame) {
                gameNameLabel.text = currentGame.name || "Unnamed Game"
                previewImage.source = currentGame.icon_path ? Qt.resolvedUrl(currentGame.icon_path).toString() : ""
                genreRepeater.updateSelectedGenres(currentGame.genre ? currentGame.genre.split(", ") : [])
                yearField.text = currentGame.year > 0 ? currentGame.year : ""
                console.log("Opened dialog for app_id:", currentGame.app_id, "currentGame:", JSON.stringify(currentGame))
            }
        }

        Platform.FileDialog {
            id: fileDialog
            title: "Select Game Image"
            nameFilters: ["Image files (*.png *.jpg *.jpeg)"]
            folder: Platform.StandardPaths.writableLocation(Platform.StandardPaths.PicturesLocation)

            onAccepted: {
                if (editDialog.currentGame && editDialog.currentGame.app_id) {
                    var sourcePath = fileDialog.file.toString().replace(/^file:\/\/\//, "")
                    console.log("Selecting icon for app_id:", editDialog.currentGame.app_id, "sourcePath:", sourcePath)
                    var newIconPath = libraryController.copyIcon(sourcePath, editDialog.currentGame.app_id)
                    if (newIconPath) {
                        previewImage.source = Qt.resolvedUrl(newIconPath).toString()
                        editDialog.currentGame.icon_path = newIconPath
                        console.log("New icon path:", newIconPath)
                    } else {
                        console.log("Failed to copy icon, keeping old path:", editDialog.currentGame.icon_path)
                    }
                } else {
                    console.log("No currentGame or app_id available")
                }
            }
        }

        ScrollView {
            id: dialogScrollView
            anchors.fill: parent
            clip: true
            ScrollBar.vertical.policy: ScrollBar.AsNeeded
            ScrollBar.horizontal.policy: ScrollBar.AsNeeded

            ColumnLayout {
                width: dialogScrollView.width
                spacing: 15
                anchors.margins: 20

                // Название игры
                Label {
                    id: gameNameLabel
                    text: "Game Name"
                    font.pixelSize: 18
                    font.bold: true
                    Layout.alignment: Qt.AlignHCenter
                }

                // Предпросмотр картинки
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Label {
                        text: "Icon Preview:"
                        font.pixelSize: 14
                    }

                    Image {
                        id: previewImage
                        width: 200
                        height: 200
                        fillMode: Image.PreserveAspectFit
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Button {
                        text: "Change Icon"
                        onClicked: {
                            fileDialog.open()
                        }
                    }
                }

                // Выбор жанра через кнопки
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Label {
                        text: "Genre:"
                        font.pixelSize: 14
                    }

                    ScrollView {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 100
                        clip: true

                        GridLayout {
                            columns: 8
                            columnSpacing: 5
                            rowSpacing: 5

                            Repeater {
                                id: genreRepeater
                                model: [
                                    "Action", "Adventure", "RPG", "Strategy", "Simulation",
                                    "Puzzle", "Platformer", "Shooter", "Racing", "Sports",
                                    "Horror", "Sandbox", "Stealth", "MMO", "Casual"
                                ]

                                property var selectedGenres: []

                                function updateSelectedGenres(genres) {
                                    selectedGenres = genres || []
                                    for (var i = 0; i < count; i++) {
                                        var button = itemAt(i)
                                        button.checked = selectedGenres.includes(button.text)
                                    }
                                }

                                Button {
                                    text: modelData
                                    checkable: true
                                    checked: genreRepeater.selectedGenres.includes(modelData)
                                    onClicked: {
                                        if (checked) {
                                            if (!genreRepeater.selectedGenres.includes(modelData)) {
                                                genreRepeater.selectedGenres.push(modelData)
                                            }
                                        } else {
                                            var index = genreRepeater.selectedGenres.indexOf(modelData)
                                            if (index !== -1) {
                                                genreRepeater.selectedGenres.splice(index, 1)
                                            }
                                        }
                                        console.log("Selected genres:", genreRepeater.selectedGenres)
                                    }

                                    background: Rectangle {
                                        color: checked ? "#d0e0ff" : "white"
                                        border.color: "gray"
                                        border.width: 1
                                        radius: 5
                                    }
                                }
                            }
                        }
                    }
                }

                // Поле для года
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Label {
                        text: "Year:"
                        font.pixelSize: 14
                    }

                    TextField {
                        id: yearField
                        Layout.preferredWidth: 100
                        validator: IntValidator { bottom: 1990 }
                        placeholderText: "Enter year (1990+)"
                    }
                }

                Button {
                    text: "Save"
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                    /*
                        if (currentGame && currentGame.app_id) {
                            var newYear = parseInt(yearField.text) || 0
                            var genresString = genreRepeater.selectedGenres.join(", ")
                            console.log("Saving metadata:", {
                                "app_id": currentGame.app_id,
                                "icon_path": currentGame.icon_path || "",
                                "genre": genresString,
                                "year": newYear
                            })
                            libraryController.saveManualMetadata(
                                currentGame.app_id,
                                currentGame.icon_path || "",
                                genresString,
                                newYear
                            )
                        } else {
                            console.log("No currentGame or app_id for saving")
                        }
                        */
                        editDialog.close()
                    }
                }
            }
        }
    }
}