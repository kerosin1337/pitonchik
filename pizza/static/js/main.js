const Store = {
    set: (name, value) => localStorage.setItem(name, JSON.stringify(value)),
    get: (name) => JSON.parse(localStorage.getItem(name)),
    remove: (name) => localStorage.removeItem(name)
}
let prod = new Vue({
    el: '#prod',
    data: {
        products: [],
        newPrice: [],
        csrf: getCookie('csrftoken'),
    },
    created: function () {
        const t = this;
        axios.get('/api/products')
            .then(function (response) {
                t.products = response.data;
                t.products.forEach(function (item) {
                    t.newPrice.push(item.price)
                    item.category.name.forEach(function (j) {
                        console.log(j)
                    })
                });
            });

    },
    methods: {
        // getPizzaUrl(ct_model, slug) {
        //     return '/add/'+ ct_model +'/' + slug + '/';
        // },
        price(i, j) {
            this.newPrice.splice(i, 1, j)
        },
        async post(slug, sizePizza, i) {
            // console.log(slug, sizePizza.target.querySelector('input[name="size"]:checked').value)
            value = sizePizza.target.querySelector('input[name="size"]:checked').value
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrf
                },
                body: JSON.stringify({
                    size: value,
                    price: this.newPrice[i]
                })
            }
            const result = await fetch('/add/' + slug + '/', requestOptions).then(qty.count++)
        }

    }
})

let qty = new Vue({
    el: '#qty',
    data: {
        cartProducts: [],
        count: 0
    },
    created: function () {
        const t = this;
        axios.get('/api/cart')
            .then(function (response) {
                t.cartProducts = response.data[0];
                // t.cartProducts.products.forEach(function (item) {
                //     t.count += item.qty
                // })
                t.count = t.cartProducts.qty
            });
    },
    methods: {
        reload() {
            const t = this;
            t.count = 0;
            axios.get('/api/cart')
                .then(function (response) {
                    t.cartProducts = response.data[0];
                    // t.cartProducts.products.forEach(function (item) {
                    //     t.count += item.qty
                    // })
                    t.count = t.cartProducts.qty
                });
        }
    }
})

let app2 = new Vue({
    el: '#street',
    data: {
        search: '',
        streets: [],
        error: 'Простите, мы доставляем в радиусе 3 км.',
        dist: 0,
        seen: true,
        // user: Object,
    },
    // created: function () {
    //     const t = this;
    //     axios.get('/api/user')
    //         .then(function (response) {
    //             if (response.data.length !== 0) {
    //                 try {
    //                     t.user = response.data[0];
    //                     // t.search = arr[0];
    //                     // t.user.entrance = arr[1];
    //                     // t.user.floor_number = arr[2];
    //                     // t.user.apartment_number = arr[3];
    //                 } catch (e) {
    //                 }
    //             }
    //         });
    // },
    methods: {
        searchStreet() {
            const requestOptions = {
                method: 'GET'
            }
//         fetch(`https:nominatim.openstreetmap.org/search?country=Россия&city=Томск&format=json&limit=3&street=${this.search}`, requestOptions)
            fetch(`https:nominatim.openstreetmap.org/search?q=Томск+${this.search}&format=json&limit=3`, requestOptions)
                .then(async response => {
                        this.streets = await response.json();
                        if (this.streets.length === 0) {
                            this.streets = [{display_name: 'Ничего не найдено.'}]
                        } else {
                            this.streets.forEach(function (item) {
                                item.display_name = item.display_name.slice(0, getListIdx(item.display_name, ',')[1])
//                            item.display_name = item.display_name.slice(0, 75)
                            })
                        }
                    }
                )
        },
        choiceStreet(str, lat, lon) {

            this.dist = getDistanceFromLatLonInKm(56.4720791, 84.96071130123357, lat, lon);
            if (this.dist < 3) {
                console.log(this.dist)
                this.search = str;
                this.streets = [];
                buy.choice = false;
                err.seen = false;
            } else {
                err.seen = true
            }
        },
        changeS() {
            buy.choice = true;
        }
    },
    watch: {
//        search(q) {
//            const requestOptions = {
//                method: 'GET'
//            }
//
//            setInterval(
//                fetch(`https://nominatim.openstreetmap.org/search?country=Россия&city=Томск&format=json&limit=100&street=${q}`, requestOptions)
//                .then(async response => {
//                        this.streets = await response.json()
//                 }
//                ), 2000
//            )
//
//        }
    }
})

let buy = new Vue({
    el: '#payment',
    data: {
        choice: true,
        select: ''
    },
    methods: {
        qwee() {
            console.log(123)
        }
    },
    watch: {
        select(q) {
            app2.seen = q !== 'self';
        }
    }
})

let err = new Vue({
    el: '#err',
    data: {
        error: 'Простите, мы доставляем в радиусе 3 км.',
        seen: false
    }
})

let basket = new Vue({
    el: '#basket',
    data: {
        cart: [],
        csrf: getCookie('csrftoken'),
    },
    created: function () {
        const t = this;
        axios.get('/api/cart')
            .then(function (response) {
                t.cart = response.data[0];
            })
    },
    methods: {
        async deleteProduct(slug, size) {
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrf
                },
                body: JSON.stringify({
                    size: size,
                })

            }
            const t = this;
            const result = await fetch('/remove-from-cart/' + slug + '/', requestOptions)
                .then(async () =>
                    await axios.get('/api/cart')
                        .then(function (response) {
                            t.cart = response.data[0];
                            qty.reload()
                        })
                );

        },
        async changeQTY(slug, size, qtyN, num) {
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrf
                },
                body: JSON.stringify({
                    size: size,
                    qty: Number(qtyN + num)
                })

            }
            const t = this;
            const result = await fetch('/change-qty/' + slug + '/', requestOptions)
                .then(
                    async () =>
                        await axios.get('/api/cart')
                            .then(function (response) {
                                t.cart = response.data[0];
                                qty.count += num;
                            })
                );
        }
    }

})


let custom = new Vue({
    el: '#custom',
    data: {
        final_cost: [],
        meat: meats,
        vegetable: vegetables,
        cheese: cheeses,
        ingredients: [],
        dough: 1,
        size: 1,
        filter: 'meat',
        csrf: getCookie('csrftoken'),
    },
    // mounted() {
    //     if (localStorage.myPizza)
    //         this.final_cost = JSON.parse(localStorage.myPizza);
    //     if (localStorage.mySize)
    //         this.size = JSON.parse(localStorage.mySize);
    //     if (localStorage.myDough)
    //         this.dough = JSON.parse(localStorage.myDough);
    //     if (localStorage.myMeat)
    //         this.meat = JSON.parse(localStorage.myMeat);
    //     if (localStorage.myCheese)
    //         this.cheese = JSON.parse(localStorage.myCheese);
    //     if (localStorage.myVegetables)
    //         this.vegetable = JSON.parse(localStorage.myVegetables);
    // },
    methods: {
        addProd(prod, price, i) {
            if (prod.trues) {
                prod.style = 'prodDel';
                this.final_cost.push({prod: prod.prod, qty: 1, cost: price});
            } else {
                const idx = this.final_cost.indexOf(this.final_cost.find(src => src.prod === prod.prod));
                console.log(idx)
                if (idx !== -1) {
                    prod.style = 'prodPlus';
                    this.final_cost.splice(idx, 1);
                }
            }

            prod.trues = !prod.trues;
            // this.save();
        },
        ingredientsList() {
            if (this.filter === 'meat') {
                return this.meat;
            } else if (this.filter === 'cheese') {
                return this.cheese;
            } else if (this.filter === 'vegetable') {
                return this.vegetable;
            }
        },
        sizeImg() {
            if (this.size === 1) {
                return {'width': '70%'}
            } else if (this.size === 1.2) {
                return {'width': '85%'}
            } else if (this.size === 1.4) {
                return {'width': '100%'}
            }
        },
        removeProd(i) {
            const idx = this.final_cost.indexOf(i);
            this.final_cost.splice(idx, 1);
            // this.save();
        },
        changeQty(i, num) {
            const idx = this.final_cost.indexOf(i);
            this.final_cost[idx].qty += num;
            if (this.final_cost[idx].qty === 0) {
                this.final_cost.splice(idx, 1)
            }
            // this.save();
        },
        doughChoice(event) {
            if (event === 0)
                this.dough = 1
            else if (event === 1)
                this.dough = 1.1
            // this.save();
        },
        sizeChoice(event) {
            if (event === 0)
                this.size = 1
            if (event === 1)
                this.size = 1.2
            else if (event === 2)
                this.size = 1.4
            // this.save();
        },
        price() {
            let price = 225;
            this.final_cost.forEach(function (item) {
                price += item.cost * item.qty
            });
            return Math.ceil(price * this.dough * this.size);
        },
        async post() {
            let doughStr;
            let sizeStr;
            let descriptionStr;
            if (this.size === 1)
                sizeStr = 25
            else if (this.size === 1.2)
                sizeStr = 30
            else if (this.size === 1.4)
                sizeStr = 35
            if (this.dough === 1)
                doughStr = 'Тонкое тесто, '
            else if (this.dough === 1.1)
                doughStr = 'Традиционное тесто, '
            descriptionStr = doughStr;
            descriptionStr += this.final_cost.map(({prod, qty}) => `${prod} ${qty}`).join(', ');
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrf
                },
                body: JSON.stringify({
                    description: descriptionStr,
                    size: sizeStr,
                    price: this.price(),
                    custom: true
                })
            }
            const result = await fetch(`/add/${randStr()}/`, requestOptions).then(qty.count++);
            this.final_cost = []
            // Store.remove('myPizza');
            // Store.remove('mySize');
            // Store.remove('myDough');
            // Store.remove('myMeat');
            // Store.remove('myCheese');
            // Store.remove('myVegetables');
        },
        // save() {
        //     Store.set('myPizza', this.final_cost);
        //     Store.set('mySize', this.size);
        //     Store.set('myDough', this.dough);
        //     Store.set('myMeat', this.meat);
        //     Store.set('myCheese', this.cheese);
        //     Store.set('myVegetables', this.vegetable);
        // },
    }
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2)
    ;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180)
}


function getListIdx(str, substr) {
    let listIdx = []
    let lastIndex = -1
    while ((lastIndex = str.indexOf(substr, lastIndex + 1)) !== -1) {
        listIdx.push(lastIndex)
    }
    return listIdx
}

function randStr() {
    let result = [];
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let charactersLength = characters.length;
    for (let i = 0; i < 5; i++) {
        result.push(characters.charAt(Math.floor(Math.random() *
            charactersLength)));
    }
    return result.join('');
}

$(document).ready(function () {

    $('#tel').inputmask("9-999-999-99-99");
});