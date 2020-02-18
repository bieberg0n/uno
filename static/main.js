const log = function (...args) {
    console.log(...args)
}

const q = function (queryName) {
    return document.querySelector(queryName)
}

const qs = function (queryName) {
    return document.querySelectorAll(queryName)
}

const toggleClass = function (query, className) {
    const classSet = new Set(query.classList)
    if (classSet.has(className)) {
        query.classList.remove(className)
    } else {
        query.classList.add(className)
    }
}

const bindClick = function (queryName, handle) {
    const querys = qs(queryName)
    querys.forEach(q => q.addEventListener('click', handle, false))
}

const colorMap = function (colorName) {
    let map = new Map()
    map.set('红', 'red')
    map.set('绿', 'green')
    map.set('黄', 'yellow')
    map.set('蓝', 'blue')
    map.set('黑', 'black')
    return map.get(colorName)
}

const showCard = function (name, card) {
    let html = `<div class="card ${colorMap(card[0])}">${card.slice(1)}</div>`

    const divs = Array.from(qs('.player')).filter(p => p.dataset['name'] === name)
    if (divs.length === 0) {
        q('.players').insertAdjacentHTML('beforeEnd', `<div class="player" data-name="${name}">
            <div class="name">${name}</div>
            ${html}
        </div>`)

    } else {
        const div = divs[0]
        const p = div.querySelector('.card')
        if (p) {
            p.remove()
        }
        div.insertAdjacentHTML('beforeEnd', html)
    }
}

const showMsg = function (name, opName, card = '', other = '') {
    if (other !== '') {
        other = ' | ' + other
    }
    // q('.message').insertAdjacentHTML('afterBegin', `<p>${name}${opName}${card}${other}</p>`)
    let textarea = q('.message')
    textarea.value += `${new Date().toLocaleTimeString()}：${name}${opName}${card}${other}\n`
    textarea.scrollTop = textarea.scrollHeight
}

const showNextPlayer = function (name) {
    let players = q('.players')
    let old = players.dataset.next
    if (old === undefined) {
        old = ''
    }
    let playerDOMs = qs('.player')
    for (let p of playerDOMs) {
        if (p.dataset.name === old) {
            p.classList.remove('next')
        } else if (p.dataset.name === name) {
            p.classList.add('next')
        }
    }
    players.dataset.next = name
}

const chooseColor = function () {
    let s = q('select')
    return s.value
}

class Client {
    constructor() {
        this.socket = io.connect({transports: ['websocket']})
        this.name = ''
        this.currentLeadPlayer = ''
        this.currentCard = ''
        this.players = []
        this.playersNums = {}
        this.cards = []

        this.socket.on('broadcast', (msg) => this.broadcastCallback(msg))

        this.socket.on('push_cards', (msg) => {
            this.cards = msg.data
            this.showCards()
        })

        bindClick('#id-button-name', () => {
            this.name = q('#id-input-name').value
            localStorage.setItem('name', this.name)
            this.socket.emit('connect_event', {name: this.name})

            toggleClass(q('.hide'), 'hide')
            toggleClass(q('.show'), 'hide')
        })

        bindClick('#id-button-draw', () => this.socket.emit('draw', {'name': this.name}))

        let s = q('#id-select-choose-color')
        s.addEventListener('change', () => this.showCards(), false)
    }

    playerHTML (player) {
        let p = player
        let num = this.playersNums[p]
        if (num === undefined) {
            num = ''
        } else if (num === 1) {
            num = 'UNO!'
        } else {
            num = num.toString()
        }
        let next = this.next === p ? 'next' : ''
        let head = `<div class="player ${next}" data-name="${p}"><div class="name">${p}：${num}</div>`
        let cardHtml = ''
        let tail = '</div>'
        if (this.currentLeadPlayer === p) {
            let card = this.currentCard
            cardHtml = `<div class="card ${colorMap(card[0] === '黑' ? card[3] : card[0])}">${card[0] === '黑' ? card.slice(1, 3) : card.slice(1)}</div>`
        }
        return head + cardHtml + tail
    }

    showPlayers () {
        let playersDiv = q('.players')
        playersDiv.innerHTML = ''

        let playersHtml = this.players.map(p => this.playerHTML(p)).join('')
        playersDiv.insertAdjacentHTML('afterBegin', playersHtml)
    }

    showCards() {
        let html = this.cards.map(card => `<div class="clickable card ${colorMap(card[0] === '黑' ? chooseColor() : card[0])}" data-card="${card}">${card.slice(1)}</div>`).join('')

        let div = q('.cards')
        div.innerHTML = ''
        div.insertAdjacentHTML('beforeEnd', html)

        bindClick('.clickable', (event) => {
            let card = event.target.dataset.card
            if (card[0] === '黑') {
                card += chooseColor()
            }
            this.socket.emit('lead', {name: this.name, card: card})
        })
    }

    broadcastCallback (msg) {
        let name = msg['name']
        let type = msg['type']

        if (type === 'lead') {
            let card = msg['card']
            this.currentLeadPlayer = name
            this.currentCard = card
            let num = msg['remainCardsNum']
            let other = ''
            if (num === 1) {
                other = `${name} UNO!`
            } else if (num === 0) {
                other = `${name} 取得了胜利！`
            } else {
                other = `手上还有 ${num} 张牌`
            }
            this.playersNums[name] = num
            showMsg(name, ' 打出了', card, other)

        } else if (type === 'join') {
            this.players = msg['players']
            showMsg(name, ' 加入了')

        } else if (type === 'draw') {
            let num = msg['remainCardsNum']
            this.playersNums[name] = num
            showMsg(name, ` 摸牌，手上有 ${num} 张牌`)

        } else if (type === 'next') {
            // showNextPlayer(name)
            this.next = name
            showMsg(`轮到 ${name} 出牌`, '')

        } else {
            showMsg(name, msg['type'])
        }
        this.showPlayers()
    }
}

const main = function () {
    let name = localStorage.getItem('name')
    if (name) {
        let input = q('#id-input-name')
        input.value = name
    }
    new Client()
}

main()
