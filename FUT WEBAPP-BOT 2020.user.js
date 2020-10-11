// ==UserScript==
// @name        FUT WEBAPP-BOT 2020
// @version     1.0
// @description Adds keyboard shortcuts to FUT Web App
// @license     MIT
// @author      MF
// @match       https://www.ea.com/fifa/ultimate-team/web-app/*
// @match       https://www.ea.com/fifa/ultimate-team/web-app/*
// @namespace   https://github.com/
// ==/UserScript==


let buy = 950;

let sell1 = 1000;
let sell2 = 1100;

var botStatus = 'stop';

let btn = document.createElement("button");
let buyField  = document.createElement("INPUT");
let sellField = document.createElement("INPUT");

const config = {
    key: {
        searchMarket:   'ArrowRight',
        goBack:         'ArrowLeft',
        up:             'ArrowUp',
        down:           'ArrowDown',
        incrementBid:   'IntlBackslash',
        decrementBid:   'ShiftLeft',
        newTest:        'ShiftRight'
    },

    lowerMinimumBid:    'clear',    // options: 'clear', 'decrement', 150

    autobuy: {
        enabled: true,
        buyNowTimes: 5,
    },

    noPlayerWarning: true,
    instantBuyNow: true,
}

// -------- do not edit the code below ---------- //

const APP_NAME = "FUT Sniper_edited";
const DEBUG_MODE = true;

window.addEventListener('keydown', (event) => {
    switch (event.code) {
        case config.key.searchMarket:
            searchMarket();
            config.autobuy.enabled ? autoBuy() : buyNow();
            break;

        case config.key.newTest:
            bot();
            break;

        case config.key.goBack:
            goBack();
            break;

        case config.key.up:
            move(event);
            break;

        case config.key.down:
            move(event);
            break;

        case config.key.decrementBid:
            if (config.lowerMinimumBid === 'clear') clearBidPrice();
            if (config.lowerMinimumBid === 'decrement') editBidPrice('decrement');
            if (config.lowerMinimumBid === 150) setBidPrice(150);
            break;

        case config.key.incrementBid:
            editBidPrice('increment');
            break;

        default:
            break;
    }
});



function startbot(vtn) {
    if(vtn.innerHTML == 'BOT')
    {
        vtn.innerHTML = "-- RUNNING --";
        botStatus = 'run';
        buy = buyField.value;
        sell2 = sellField.value;
        if (isPageTitle("SEARCH RESULTS")) {
           goBack();
        }
        runBot();
    }

}


function moveToTransferlist(){
    var transfers = document.getElementsByClassName('ut-tab-bar-item icon-transfer')[0];
    tapElement(transfers);
    var transferlist = document.getElementsByClassName('tile col-1-2 ut-tile-transfer-list')[0];
    setTimeout(tapElement(transferlist),5000);
    }

function fillPrices(bid1, bid2, buy1, buy2)
{
    if (!isPageTitle("SEARCH THE TRANSFER MARKET")) {
        return;
    }
    let possibleBids = [200,250,300,350,400,'', 500, 450, 150];
    let randomVar = Math.floor(Math.random() * 8);
    bid1 = possibleBids[randomVar];
    let inputFields = document.getElementsByTagName('input')
    let minBid = inputFields[3];
    let maxBid = inputFields[4];
    let minBuy = inputFields[5];
    let maxBuy = inputFields[6];
    minBid.value = bid1;
    maxBid.value = bid2;
    minBuy.value = buy1;
    maxBuy.value = buy;
    editBidPrice('increment');

}


function editBuyPricePlus()
{
    let inputfiled = document.getElementsByClassName('btn-standard increment-value')[3];
    let sss = inputfiled.querySelector('.btn-standard.increment-value');
    tapElement(inputfiled);
}

function editBuyPriceMinus()
{
    let inputfiled = document.getElementsByClassName('btn-standard decrement-value')[3];
    let sss = inputfiled.querySelector('.btn-standard.decrement-value');
    tapElement(inputfiled);
}

function sleep(milliseconds) {
    let timeStart = new Date().getTime();
    while (true) {
        let elapsedTime = new Date().getTime() - timeStart;
        if (elapsedTime > milliseconds) {
            break;
        }
    }
}

function pressPositionChange()
{
    let p = document.getElementsByClassName('ut-search-filter-control--row');
    let tappy1 = p[0].querySelector('.ut-search-filter-control--row-button');

    sendTouchEvent(tappy1, 'touchstart');
    sendTouchEvent(tappy1, 'touchstart');
    sendTouchEvent(tappy1, 'touchend');
    let positionChange = document.getElementsByTagName('ul')[2].childNodes[2];
    tapElement(positionChange);
}


function pressPosition()
{
    let p2 = document.getElementsByClassName('ut-search-filter-control--row');
    let tappy2 = p2[2].querySelector('.ut-search-filter-control--row-button');
    sendTouchEvent(tappy2, 'touchstart');
    sendTouchEvent(tappy2, 'touchstart');
    sendTouchEvent(tappy2, 'touchend');
    let cdm_cm = document.getElementsByTagName('ul')[2].childNodes[16]
    tapElement(cdm_cm)
}

function createButton(){
    let buttonLocation = document.querySelector('.menu-container');
    btn.innerHTML = "BOT";
    btn.type = "button";
    btn.onclick = function() {startbot(btn)};
    buttonLocation.insertBefore(btn,buttonLocation.childNodes[0]);

    buyField.setAttribute("type", "text");
    sellField.setAttribute("type", "text");

    let inputfield = document.querySelector('.menu-container');
    inputfield.insertBefore(document.createElement('br'),inputfield.childNodes[0]);
    inputfield.insertBefore(sellField,inputfield.childNodes[0]);
    inputfield.insertBefore(document.createElement('br'),inputfield.childNodes[0]);
    inputfield.insertBefore(buyField,inputfield.childNodes[0]);



}

function searchList()
{
    var playerlist = document.getElementsByClassName('paginated-item-list ut-pinned-list')[0].childNodes[0].childNodes;
    // see content with innerText
    var time       = playerlist[1].getElementsByClassName('time')[0].innerText; // 'Expired'
    var currentBid = playerlist[1].getElementsByClassName('currency-coins value')[0].innerText;
    var bidstatus  = playerlist[1].getElementsByClassName('name');
    var className  = playerlist[1].className();
    // listFUTItem has-auction-data selected outbid
    // listFUTItem has-auction-data highest-bid
    // listFUTItem has-auction-data expired
    // listFUTItem has-auction-data highest-bid
    // listFUTItem has-auction-data

    return playerlist;
}


function wonCheck()
{
    try
    {
    return document.getElementsByClassName('subHeading')[0].innerHTML == "Congratulations, you've won this item for";
    }
    catch(error)
    {
        log('no WON')
        return false;
    }
}

function listItem()
{
    if(wonCheck() == true)
    {
        var buyedPrice = parseInt(document.getElementsByClassName('currency-coins subContent')[0].childNodes[0].data)

        let listButton = document.getElementsByClassName('accordian')[0];
        if (!listButton)
        {
            log("The List Button was not found 1", true);
            return;
        }
        setTimeout(tapElement(listButton), 2000);

        document.getElementsByClassName('numericInput filled')[0].value = sell2 - 250;
        document.getElementsByClassName('numericInput filled')[1].value = sell2;
        let listEnd = document.querySelector('.btn-standard.call-to-action');
        if (!listEnd)
        {
            log("The List Button was not found 2", true);
            return;
        }
        setTimeout(tapElement(listEnd), 3000);
        try{
            var found = document.querySelector('.ut-no-results-view') == null;
            if (!found)
            {
                var found2 = document.querySelector('.ut-no-results-view').innerText.indexOf('No results found')
                if (found2 !== 0)
                {


                }
            }
        }
        catch(error)
        {
            log('TF full');
        }
        log('go back');
        setTimeout(goBack, 6000);
        setTimeout(editBidPrice('increment'), 6100);
    }
}


function runBot()
{
    clearBidPrice();
    //pressPositionChange();
    let delay2 = 2000;
    //setTimeout(pressPosition,delay2);
    var delay = 2000;
    delay2 = delay +delay2;
    for (let i = 0; i < 20; i++) {
        setTimeout(() =>{
            fillPrices(200, '', '', buy);
            editBuyPricePlus();
            editBuyPriceMinus();
            searchMarket();
            config.autobuy.enabled ? autoBuyNew() : buyNowNew();
        }, delay2);
        delay2 = delay2 + delay;
    }
    setTimeout(() =>
               {
        btn.innerHTML = "BOT";
    }, delay2);


}

const bot = () =>{
    createButton();
}


/**
 * Simulate a click on Search button on transfer page
 */
const searchMarket = () => {
    if (!isPageTitle("SEARCH THE TRANSFER MARKET")) {
        return;
    }

    const searchButton = document.querySelector('.btn-standard.call-to-action');

    if (!searchButton) {
        log("The search button was not found", true);
        return;
    }

    if (config.noPlayerWarning) {
        const playerName = document.querySelector('.ut-text-input-control').value;

        //if (playerName.length < 1) {
        //    if (confirm("Kein Spieler wurde ausgewählt, trotzdem fortfahren?") !== true) {
        //        return;
        //    }

        //}
    }

    log("Search button found, attempting to search the market...");

    tapElement(searchButton);
}

/**
 * Automatically buy first player in search results
 */
const autoBuy = () => {
    const numberOfTimes = config.autobuy.buyNowTimes;
    let delay = 200; // ms

    for (let i = 0; i < numberOfTimes; i++) {
        setTimeout(buyNow, delay);
        log(i);
        delay = delay + 200;
    }
    delay = delay + 50;
    log(delay);
    setTimeout(noResult, delay);
}


const autoBuyNew = () => {
    const numberOfTimes = config.autobuy.buyNowTimes;
    let delay = 200; // ms

    for (let i = 0; i < numberOfTimes; i++) {
        setTimeout(buyNow, delay);
        delay = delay + 200;
    }
    delay = delay + 50;
    setTimeout(noResult, delay);
    delay = delay + 2000;
    setTimeout(listItem, delay);

}

/**
 * Simulate a click on buy now button on selected items card
 */

const buyNow = () => {
    if (!isPageTitle("SEARCH RESULTS")) {
        return;
    }

    const buyNowButton = document.querySelector('.btn-standard.buyButton.currency-coins');

    if (!buyNowButton) {
        //log("No buy now button was found.", true);
        return;
    }

    log("Attempting to buy the card...");

    tapElement(buyNowButton);
}


function noResult()
{
    //log('lets check');
    var found = document.querySelector('.ut-no-results-view') == null;
    if (!found){
        //log('lets check2');
        var found2 = document.querySelector('.ut-no-results-view').innerText.indexOf('No results found')
        if (found2 == 0)
        {
            log('Nothing found -> Go Back')
            goBack();
            //setTimeout(goBack, 500);
            setTimeout(editBidPrice('increment'), 1000);
        }
        return true;
    }
}

const buyNowNew = () => {
    if (!isPageTitle("SEARCH RESULTS")) {
        return;
    }



    const buyNowButton = document.querySelector('.btn-standard.buyButton.currency-coins');

    if (!buyNowButton) {
        log("No buy now button was found.", true);
        return;
    }

    log("Attempting to buy the card...");

    tapElement(buyNowButton);
}


/**
 * Goes back.
 */
const goBack = () => {
    if (!isPageTitle("SEARCH RESULTS")) {
        return;
    }

    log('Attempting to go to the previous page...');

    try {
        const backButton = document.getElementsByClassName('ut-navigation-button-control')[0];
        tapElement(backButton);
    } catch (error) {
        log('Unable to go back.', true);
        return;
    }

    log('Successfully went back.');
}

/**
 * Change selected item on search results
 * @param {Event} event
 */
const move = (event) => {
    try {
        const isDown = event.keyCode === 40;

        const itemList = document.querySelector('.ut-pinned-list > ul');
        const items = Array.from(itemList.getElementsByClassName('listFUTItem'));

        let currentIndex = items.findIndex((item) => {
            return item.className.indexOf('selected') > -1;
        });

        if (isDown && currentIndex + 1 <= items.length) {
            const div = items[++currentIndex].getElementsByClassName('has-tap-callback')[0];
            tapElement(div);
        } else if (!isDown && currentIndex - 1 >= 0) {
            const div = items[--currentIndex].getElementsByClassName('has-tap-callback')[0];
            tapElement(div);
        }
    } catch (error) {
        log('Unable to change the currently selected item...', true);
        return;
    }

    log('Successfully changed the currently selected item.');
}

/**
 * Set a minimum bid price
 * @param {integer} value
 */
const setBidPrice = (value) => {
    const inputField = document.querySelector('.numericInput');

    inputField.value = value;
}

const getBidPrice = () => {
    const inputField = document.querySelector('.numericInput');

    return inputField.value;
}

/**
 * Increment or decrement the minimum bid price
 * @param {string} type
 */
const editBidPrice = (type) => {
    //const btns = document.getElementsByClassName('btn-standard ' + 'increment' + '-value')[2];
    const btn = document.querySelector('.btn-standard.' + type + '-value');

    try{
        tapElement(btn);;
        }
    catch(error)
    {
        log('edit Bid Price not found')
    }
}

/**
 * Clear the minimum bid price.
 */
const clearBidPrice = () => {
    const clearBtn = document.querySelector('.search-price-header > .flat.camel-case');

    tapElement(clearBtn);
}

/**
 * Check if current page title is equal to provided value
 * @param {string} title
 */
const isPageTitle = (title) => {
    const currentPageTitle = document.querySelector('h1.title').innerText;

    return currentPageTitle === title;
}

const notFound = (title) => {
    const itemList = document.querySelector('.ut-pinned-list > ul');
    const items = Array.from(itemList.getElementsByClassName('listFUTItem'));
    if (!items) {
        return 1 == 1;
    }

    return true;
}

/**
 * Add custom css styling
 */
const improveStyling = () => {
    const style = document.createElement('style');
    style.innerHTML = `
        .ut-content-container { padding: 0; }
        .ut-content-container .ut-content { border: 0; }
        .ut-content-container .ut-content.ut-content--split-view-extend { max-height: 100%; }
        .listFUTItem .entityContainer .name.untradeable { display: block;}
        .listFUTItem .entityContainer .name.untradeable::before { position: relative; padding-right: 10px; }
        .ut-club-search-results-view.ui-layout-left .listFUTItem .entityContainer,
        .ut-unassigned-view.ui-layout-left .listFUTItem .entityContainer { width: 45%; }
        @media (min-width: 1281px) {
            .ut-content-container .ut-content { max-width: 100%; max-height: 100%;  }
            .ut-split-view .ut-content { max-width: 100%; max-height: 100%; }
      }
    `;
    document.head.appendChild(style);
}

/**
 * Logs a message to the console with app information.
 *
 * @param {string} message
 * @param {boolean} isError
 */
const log = (message, isError) => {
    if (!DEBUG_MODE) {
        return;
    }

    let logFunction = console.info;

    if (isError) {
        logFunction = console.error;
    }

    logFunction(`${APP_NAME}: ${message}`)
}

/**
 * Simulates a tap/click on an element.
 *
 * @param {HTMLElement} element
 */
const tapElement = (element) => {
    sendTouchEvent(element, 'touchstart');
    sendTouchEvent(element, 'touchend');
}

/**
 * Dispatches a touch event on the element.
 * https://stackoverflow.com/a/42447620
 *
 * @param {HTMLElement} element
 * @param {string} eventType
 */
const sendTouchEvent = (element, eventType) => {
    const touchObj = new Touch({
        identifier: 'Keyboard shortcuts should be supported natively without an extension!',
        target: element,
        clientX: 0,
        clientY: 0,
        radiusX: 2.5,
        radiusY: 2.5,
        rotationAngle: 10,
        force: 0.5
    });

    const touchEvent = new TouchEvent(eventType, {
        cancelable: true,
        bubbles: true,
        touches: [touchObj],
        targetTouches: [touchObj],
        changedTouches: [touchObj],
        shiftKey: true
    });

    element.dispatchEvent(touchEvent);
}

/**
 * Instant buy now functionality
 */
if (config.instantBuyNow) {
    utils.PopupManager.ShowConfirmation = (dialog, amount, proceed, s) => {
        let cancel = s;

        if (!utils.JS.isFunction(s)) {
            cancel = function () { };
        }

        if (dialog.title === utils.PopupManager.Confirmations.CONFIRM_BUY_NOW.title) {
            proceed();
            return;
        }

        const n = new controllers.views.popups.Dialog(
            dialog.message, dialog.title,
            enums.UIDialogTypes.MESSAGE, amount, dialog.buttonLabels,
        );
        n.init();
        gPopupClickShield.setActivePopup(n);
        n.onExit.observe(this, (e, t) => {
            if (t !== enums.UIDialogOptions.CANCEL && t !== enums.UIDialogOptions.NO) {
                if (proceed) {
                    proceed();
                } else if (cancel) {
                    cancel();
                }
            }
        });
    };
}
// Call the function to edit css...
improveStyling();