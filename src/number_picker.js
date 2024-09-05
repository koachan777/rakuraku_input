/*!
 * Picker.js v1.2.1
 * https://fengyuanchen.github.io/pickerjs
 *
 * Copyright 2016-present Chen Fengyuan
 * Released under the MIT license
 *
 * Date: 2019-02-18T13:08:12.801Z
 */
! function(e, t) {
	"object" == typeof exports && "undefined" != typeof module ? module.exports =
		t() : "function" == typeof define && define.amd ? define(t) : (e = e || self)
		.Picker = t()
}(this, function() {
	"use strict";

	function t(e) {
		return (t = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ?
			function(e) {
				return typeof e
			} : function(e) {
				return e && "function" == typeof Symbol && e.constructor === Symbol && e !==
					Symbol.prototype ? "symbol" : typeof e
			})(e)
	}

	function r(e, t) {
		for (var n = 0; n < t.length; n++) {
			var i = t[n];
			i.enumerable = i.enumerable || !1, i.configurable = !0, "value" in i && (i.writable = !
				0), Object.defineProperty(e, i.key, i)
		}
	}

	function n(e) {
		return function(e) {
			if (Array.isArray(e)) {
				for (var t = 0, n = new Array(e.length); t < e.length; t++) n[t] = e[t];
				return n
			}
		}(e) || function(e) {
			if (Symbol.iterator in Object(e) || "[object Arguments]" === Object.prototype
				.toString.call(e)) return Array.from(e)
		}(e) || function() {
			throw new TypeError("Invalid attempt to spread non-iterable instance")
		}()
	}
	var a = {
			container: null,
			controls: !1,
			date: null,
			format: "YYYY-MM-DD HH:mm",
			headers: !1,
			increment: 1,
			inline: !1,
			language: "",

			rows: 5,
			text: {
				title: "Pick a date and time",
				cancel: "Cancel",
				confirm: "OK",

				minute: "Minute",
				second: "Second",
				millisecond: "Millisecond"
			},
			translate: function(e, t) {
				return t
			},
			show: null,
			shown: null,
			hide: null,
			hidden: null,
			pick: null
		},
		v =
		'<div class="picker" data-picker-action="hide" touch-action="none" tabindex="-1" role="dialog"><div class="picker-dialog" role="document"><div class="picker-header"><h4 class="picker-title">{{ title }}</h4><button type="button" class="picker-close" data-picker-action="hide" aria-label="Close">&times;</button></div><div class="picker-body"><div class="picker-grid"></div></div><div class="picker-footer"><button type="button" class="picker-cancel" data-picker-action="hide">{{ cancel }}</button><button type="button" class="picker-confirm" data-picker-action="pick">{{ confirm }}</button></div></div></div>',
		s = "undefined" != typeof window,
		g = s ? window : {},
		e = !!s && "ontouchstart" in g.document.documentElement,
		i = !!s && "PointerEvent" in g,
		b = "picker",
		o = {},
		y = "next",
		k = "prev",
		w = "".concat(b, "-open"),
		M = "".concat(b, "-opened"),
		d = "".concat(b, "-picked"),
		E = "".concat(b, "Action"),
		Y = "type",
		m = "value",
		c = "click",
		l = "focus",
		h = "hidden",
		u = "hide",
		f = "keydown",
		p = "pick",
		x = i ? "pointerdown" : e ? "touchstart" : "mousedown",
		D = i ? "pointermove" : e ? "touchmove" : "mousemove",
		S = i ? "pointerup pointercancel" : e ? "touchend touchcancel" : "mouseup",
		C = "show",
		N = "shown",
		A = "wheel mousewheel DOMMouseScroll",
		O = Object.prototype,
		H = O.hasOwnProperty,
		P = O.toString;

	function F(e) {
		return "string" == typeof e
	}
	var L = Number.isFinite || g.isFinite,
		j = Number.isNaN || g.isNaN;

	function T(e) {
		return "number" == typeof e && !j(e)
	}

	function _(e) {
		return "object" === t(e) && null !== e
	}

	function B(e) {
		if (!_(e)) return !1;
		try {
			var t = e.constructor,
				n = t.prototype;
			return t && n && H.call(n, "isPrototypeOf")
		} catch (e) {
			return !1
		}
	}

	function V(e) {
		return "function" == typeof e
	}

	function I(e) {
		return "date" === (t = e, P.call(t).slice(8, -1).toLowerCase());
		var t
	}

	function R(t, n) {
		if (t && V(n))
			if (Array.isArray(t) || T(t.length)) {
				var e, i = t.length;
				for (e = 0; e < i && !1 !== n.call(t, t[e], e, t); e += 1);
			} else _(t) && Object.keys(t).forEach(function(e) {
				n.call(t, t[e], e, t)
			});
		return t
	}

	function W(n) {
		for (var e = arguments.length, t = new Array(1 < e ? e - 1 : 0), i = 1; i <
			e; i++) t[i - 1] = arguments[i];
		return _(n) && 0 < t.length && t.forEach(function(t) {
			_(t) && Object.keys(t).forEach(function(e) {
				B(n[e]) && B(t[e]) ? n[e] = W({}, n[e], t[e]) : n[e] = t[e]
			})
		}), n
	}

	function J(e, t) {
		if (t)
			if (T(e.length)) R(e, function(e) {
				J(e, t)
			});
			else if (e.classList) e.classList.add(t);
		else {
			var n = e.className.trim();
			n ? n.indexOf(t) < 0 && (e.className = "".concat(n, " ").concat(t)) : e.className =
				t
		}
	}

	function q(e, t) {
		t && (T(e.length) ? R(e, function(e) {
				q(e, t)
			}) : e.classList ? e.classList.remove(t) : 0 <= e.className.indexOf(t) &&
			(e.className = e.className.replace(t, "")))
	}
	var K = /([a-z\d])([A-Z])/g;

	function U(e) {
		return e.replace(K, "$1-$2").toLowerCase()
	}

	function $(e, t) {
		return _(e[t]) ? e[t] : e.dataset ? e.dataset[t] : e.getAttribute("data-".concat(
			U(t)))
	}

	function z(e, t, n) {
		_(n) ? e[t] = n : e.dataset ? e.dataset[t] = n : e.setAttribute("data-".concat(
			U(t)), n)
	}
	var Z = /\s\s*/,
		G = function() {
			var e = !1;
			if (s) {
				var t = !1,
					n = function() {},
					i = Object.defineProperty({}, "once", {
						get: function() {
							return e = !0, t
						},
						set: function(e) {
							t = e
						}
					});
				g.addEventListener("test", n, i), g.removeEventListener("test", n, i)
			}
			return e
		}();

	function Q(n, e, i) {
		var r = 3 < arguments.length && void 0 !== arguments[3] ? arguments[3] : {},
			a = i;
		e.trim().split(Z).forEach(function(e) {
			if (!G) {
				var t = n.listeners;
				t && t[e] && t[e][i] && (a = t[e][i], delete t[e][i], 0 === Object.keys(
					t[e]).length && delete t[e], 0 === Object.keys(t).length && delete n.listeners)
			}
			n.removeEventListener(e, a, r)
		})
	}

	function X(a, e, s) {
		var o = 3 < arguments.length && void 0 !== arguments[3] ? arguments[3] : {},
			c = s;
		e.trim().split(Z).forEach(function(i) {
			if (o.once && !G) {
				var e = a.listeners,
					r = void 0 === e ? {} : e;
				c = function() {
						delete r[i][s], a.removeEventListener(i, c, o);
						for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++) t[
							n] = arguments[n];
						s.apply(a, t)
					}, r[i] || (r[i] = {}), r[i][s] && a.removeEventListener(i, r[i][s], o),
					r[i][s] = c, a.listeners = r
			}
			a.addEventListener(i, c, o)
		})
	}

	function ee(e, t, n) {
		var i;
		return V(Event) && V(CustomEvent) ? i = new CustomEvent(t, {
				detail: n,
				bubbles: !0,
				cancelable: !0
			}) : (i = document.createEvent("CustomEvent")).initCustomEvent(t, !0, !0, n),
			e.dispatchEvent(i)
	}

	function ne(e) {
		var t = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : 1,
			n = String(Math.abs(e)),
			i = n.length,
			r = "";
		for (e < 0 && (r += "-"); i < t;) i += 1, r += "0";
		return r + n
	}

	function ie(e) {
		return {

			m: "minute",
			s: "second",
			S: "millisecond"
		}[e.charAt(0)]
	}
	var re = /(Y|M|D|H|m|s|S)\1*/g;
	var ae = {
			bind: function() {
				var e = this.element,
					t = this.options,
					n = this.grid;
				V(t.show) && X(e, C, t.show), V(t.shown) && X(e, N, t.shown), V(t.hide) &&
					X(e, u, t.hide), V(t.hidden) && X(e, h, t.hidden), V(t.pick) && X(e, p,
						t.pick), X(e, l, this.onFocus = this.focus.bind(this)), X(e, c, this.onFocus),
					X(this.picker, c, this.onClick = this.click.bind(this)), X(n, A, this.onWheel =
						this.wheel.bind(this)), X(n, x, this.onPointerDown = this.pointerdown.bind(
						this)), X(document, D, this.onPointerMove = this.pointermove.bind(this)),
					X(document, S, this.onPointerUp = this.pointerup.bind(this)), X(document,
						f, this.onKeyDown = this.keydown.bind(this))
			},
			unbind: function() {
				var e = this.element,
					t = this.options,
					n = this.grid;
				V(t.show) && Q(e, C, t.show), V(t.shown) && Q(e, N, t.shown), V(t.hide) &&
					Q(e, u, t.hide), V(t.hidden) && Q(e, h, t.hidden), V(t.pick) && Q(e, p,
						t.pick), Q(e, l, this.onFocus), Q(e, c, this.onFocus), Q(this.picker, c,
						this.onClick), Q(n, A, this.onWheel), Q(n, x, this.onPointerDown), Q(
						document, D, this.onPointerMove), Q(document, S, this.onPointerUp), Q(
						document, f, this.onKeyDown)
			}
		},
		se = {
			focus: function(e) {
				e.target.blur(), this.show()
			},
			click: function(e) {
				var t = e.target,
					n = $(t, E);
				switch (n) {
					case "hide":
						this.hide();
						break;
					case "pick":
						this.pick();
						break;
					case k:
					case y:
						this[n]($(t.parentElement, Y))
				}
			},
			wheel: function(e) {
				var t = e.target;
				if (t !== this.grid) {
					for (e.preventDefault(); t.parentElement && t.parentElement !== this.grid;)
						t = t.parentElement;
					var n = $(t, Y);
					e.deltaY < 0 ? this.prev(n) : this.next(n)
				}
			},
			pointerdown: function(e) {
				var t = e.target;
				if (t !== this.grid && !$(t, E)) {
					for (e.preventDefault(); t.parentElement && t.parentElement !== this.grid;)
						t = t.parentElement;
					var n = t.querySelector(".".concat(b, "-list")),
						i = n.firstElementChild.offsetHeight;
					this.cell = {
						elem: t,
						list: n,
						moveY: 0,
						maxMoveY: i,
						minMoveY: i / 2,
						startY: e.changedTouches ? e.changedTouches[0].pageY : e.pageY,
						type: $(t, Y)
					}
				}
			},
			pointermove: function(e) {
				var t = this.cell;
				if (t) {
					e.preventDefault();
					var n = e.changedTouches ? e.changedTouches[0].pageY : e.pageY,
						i = t.moveY + (n - t.startY);
					t.startY = n, t.moveY = i, Math.abs(i) < t.maxMoveY ? t.list.style.top =
						"".concat(i, "px") : (t.list.style.top = 0, t.moveY = 0, i >= t.maxMoveY ?
							this.prev(t.type) : i <= -t.maxMoveY && this.next(t.type))
				}
			},
			pointerup: function(e) {
				var t = this.cell;
				t && (e.preventDefault(), t.list.style.top = 0, t.moveY >= t.minMoveY ?
					this.prev(t.type) : t.moveY <= -t.minMoveY && this.next(t.type), this.cell =
					null)
			},
			keydown: function(e) {
				!this.shown || "Escape" !== e.key && 27 !== e.keyCode || this.hide()
			}
		},
		oe = {
			render: function(e) {
				var t = this;
				if (e) {
					var n = this.options,
						i = this.data[e],
						r = this.current(e),
						a = V(i.max) ? i.max() : i.max,
						s = V(i.min) ? i.min() : i.min,
						o = 0;
					L(a) && (o = 0 < s ? a : a + 1), i.list.innerHTML = "", i.current = r;
					for (var c = 0; c < n.rows + 2; c += 1) {
						var l = document.createElement("li"),
							h = c - i.index,
							u = r + h * i.increment;
						o && (u %= o) < s && (u += o), l.textContent = n.translate(e, i.aliases ?
								i.aliases[u] : ne(u + i.offset, i.digit)), z(l, "name", e), z(l, m, u),
							J(l, "".concat(b, "-item")), 0 === h && (J(l, d), i.item = l), i.list.appendChild(
								l)
					}
				} else this.format.tokens.forEach(function(e) {
					return t.render(ie(e))
				})
			},
			current: function(e, t) {
				var n = this.date,
					i = this.format,
					r = i[e];
				switch (r.charAt(0)) {

					case "m":
						return T(t) && n.setMinutes(t), n.getMinutes();
					case "s":
						return T(t) && n.setSeconds(t), n.getSeconds();
					case "S":
						return T(t) && n.setMilliseconds(t), n.getMilliseconds()
				}
				return n
			},
			getValue: function() {
				var e = this.element;
				return this.isInput ? e.value : e.textContent
			},
			setValue: function(e) {
				var t = this.element;
				this.isInput ? t.value = e : this.options.container && (t.textContent = e)
			},
			open: function() {
				var e = this.body;
				e.style.overflow = "hidden", e.style.paddingRight = "".concat(this.scrollBarWidth +
					(parseFloat(this.initialBodyPaddingRight) || 0), "px")
			},
			close: function() {
				var e = this.body;
				e.style.overflow = "", e.style.paddingRight = this.initialBodyPaddingRight
			}
		},
		ce = {
			show: function() {
				var e = 0 < arguments.length && void 0 !== arguments[0] && arguments[0],
					t = this.element,
					n = this.picker;
				if (this.inline || this.shown) return this;
				if (!1 === ee(t, C)) return this;
				this.shown = !0, this.open(), J(n, w);
				var i = function() {
					ee(t, N)
				};
				return e || n.offsetWidth, J(n, M), e ? i() : setTimeout(i, 300), this
			},
			hide: function() {
				var e = this,
					t = 0 < arguments.length && void 0 !== arguments[0] && arguments[0],
					n = this.element,
					i = this.picker;
				if (this.inline || !this.shown) return this;
				if (!1 === ee(n, u)) return this;
				this.shown = !1, q(i, M);
				var r = function() {
					e.close(), q(i, w), ee(n, h)
				};
				return t ? r() : setTimeout(r, 300), this
			},
			prev: function(e) {
				var t = this.options,
					n = this.format[e],
					i = this.data[e],
					r = i.list,
					a = r.lastElementChild,
					s = V(i.max) ? i.max() : i.max,
					o = V(i.min) ? i.min() : i.min,
					c = i.item.previousElementSibling,
					l = Number($(r.firstElementChild, m)) - i.increment;
				return l < o && (l += s - o + 1), a.textContent = t.translate(e, i.aliases ?
						i.aliases[l] : ne(l + i.offset, n.length)), z(a, m, l), c && (q(i.item,
						d), J(c, d), i.item = c), r.insertBefore(a, r.firstElementChild), i.current =
					Number($(i.item, m)), this.current(e, i.current), this.inline && t.container &&
					this.pick(), this
			},
			next: function(e) {
				var t = this.options,
					n = this.format[e],
					i = this.data[e],
					r = i.list,
					a = r.firstElementChild,
					s = V(i.max) ? i.max() : i.max,
					o = V(i.min) ? i.min() : i.min,
					c = i.item.nextElementSibling,
					l = Number($(r.lastElementChild, m)) + i.increment;
				return s < l && (l -= s - o + 1), a.textContent = t.translate(e, i.aliases ?
						i.aliases[l] : ne(l + i.offset, n.length)), z(a, m, l), r.appendChild(a),
					c && (q(i.item, d), J(c, d), i.item = c), i.current = Number($(i.item, m)),
					this.current(e, i.current), this.inline && t.container && this.pick(),
					this
			},
			pick: function() {
				var e = this.element;
				if (!1 === ee(e, p)) return this;
				var t = this.formatDate(this.date);
				return this.setValue(t), this.isInput && !1 === ee(e, "change") && this.reset(),
					this.hide(), this
			},
			getDate: function() {
				var e = 0 < arguments.length && void 0 !== arguments[0] && arguments[0],
					t = this.date;
				return e ? this.formatDate(t) : new Date(t)
			},
			
			update: function() {
				return this.date = this.parseDate(this.getValue()), this.render(), this
			},

			parseDate: function(o) {
				var c = this.options,
					l = this.format,
					e = [];
				if (I(o)) return new Date(o);

				var h = new Date;
				return e.forEach(function(e, t) {
					var n = l.tokens[t],
						i = Number(e);
					switch (n) {

						case "mm":
						case "m":
							h.setMinutes(i);
							break;
						case "ss":
						case "s":
							h.setSeconds(i);
							break;
						case "SSS":
						case "SS":
						case "S":
							h.setMilliseconds(i)
					}
				}), h
			},
			formatDate: function(e) {
				var t, n = this.options,
					i = this.format,
					r = "";
				if (I(t = e) && "Invalid Date" !== t.toString()) {
					var 						l = e.getMinutes(),
						h = e.getSeconds(),
						u = e.getMilliseconds();
					r = n.format, i.tokens.forEach(function(e) {
						var t = "";
						switch (e) {
		
							case "mm":
							case "m":
								t = ne(l, e.length);
								break;
							case "ss":
							case "s":
								t = ne(h, e.length);
								break;
							case "SSS":
							case "SS":
							case "S":
								t = ne(u, e.length)
						}
						r = r.replace(e, t)
					})
				}
				return r
			},
			destroy: function() {
				var e = this.element,
					t = this.picker;
				return $(e, b) && (this.hide(!0), this.unbind(), function(t, n) {
					if (_(t[n])) try {
						delete t[n]
					} catch (e) {
						t[n] = void 0
					} else if (t.dataset) try {
						delete t.dataset[n]
					} catch (e) {
						t.dataset[n] = void 0
					} else t.removeAttribute("data-".concat(U(n)))
				}(e, b), t.parentNode.removeChild(t)), this
			}
		},
		le = /\{\{\s*(\w+)\s*\}\}/g,
		he = /input|textarea/i,
		ue = g.Picker,
		de = function() {
			function n(e) {
				var t = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {};
				if (function(e, t) {
						if (!(e instanceof t)) throw new TypeError(
							"Cannot call a class as a function")
					}(this, n), !e || 1 !== e.nodeType) throw new Error(
					"The first argument is required and must be an element.");
				this.element = e, this.options = W({}, a, o[t.language], B(t) && t), this.shown = !
					1, this.init()
			}
			var e, t, i;
			return e = n, i = [{
				key: "noConflict",
				value: function() {
					return g.Picker = ue, n
				}
			}, {
				key: "setDefaults",
				value: function(e) {
					W(a, o[e.language], B(e) && e)
				}
			}], (t = [{
				key: "init",
				value: function() {
					var l = this,
						e = this.element;
					if (!$(e, b)) {
						z(e, b, this);
						var h = this.options,
							t = he.test(e.tagName),
							n = h.inline && (h.container || !t),
							i = document.createElement("div");
						i.insertAdjacentHTML("afterbegin", v.replace(le, function() {
							for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
								t[n] = arguments[n];
							return h.text[t[1]]
						}));
						var r = i.getElementsByClassName(b)[0],
							u = r.getElementsByClassName("".concat(b, "-grid"))[0],
							a = h.container;
						if (F(a) && (a = document.querySelector(a)), n) J(r, w), J(r, M), a ||
							(a = e);
						else {
							var s = e.ownerDocument,
								o = s.body || s.documentElement;
							this.body = o, this.scrollBarWidth = g.innerWidth - s.documentElement
								.clientWidth, this.initialBodyPaddingRight = g.getComputedStyle(o)
								.paddingRight, J(r, "".concat(b, "-fixed")), a || (a = document.body)
						}
						this.isInput = t, this.inline = n, this.container = a, this.picker =
							r, this.grid = u, this.cell = null, this.format = function(e) {
								var n = e.match(re);
								if (!n) throw new Error("Invalid format.");
								var t = {
									tokens: n = n.filter(function(e, t) {
										return n.indexOf(e) === t
									})
								};
								return n.forEach(function(e) {
									t[ie(e)] = e
								}), t
							}(h.format);
						var c = this.getValue(),
							d = this.parseDate(h.date || c);
						this.date = d, this.initialDate = new Date(d), this.initialValue = c,
							this.data = {};
						var m = Number(h.rows);
						m % 2 || (m += 1), h.rows = m || 5, J(u, "".concat(b, "-").concat(1 <
							h.rows ? "multiple" : "single")), h.controls && J(u, "".concat(b,
							"-controls"));
						var f = h.headers,
							p = h.increment;
						f && (J(u, "".concat(b, "-headers")), f = B(f) ? f : h.text), B(p) ||
							(p = {
								minute: p,
								second: p,
								millisecond: p
							}), this.format.tokens.forEach(function(e) {
								var t = ie(e),
									n = document.createElement("div"),
									i = document.createElement("div"),
									r = document.createElement("ul"),
									a = {
										digit: e.length,
										increment: Math.abs(Number(p[t])) || 1,
										list: r,
										max: 1 / 0,
										min: -1 / 0,
										index: Math.floor((h.rows + 2) / 2),
										offset: 0
									};
								switch (e.charAt(0)) {
									case "s":
										a.max = 99, a.min = 0;
										break;
									case "S":
										a.max = 99, a.min = 0
                                        break;
                                    case "d": // 新たに小数点以下第1位の桁を扱う
										a.max = 9.9, a.min = 0;
										break;
								}
								if (z(n, Y, t), z(n, "token", e), f) {
									var s = document.createElement("div");
									J(s, "".concat(b, "-cell__header")), s.textContent = f[t] || t[0]
										.toUpperCase() + t.substr(1), n.appendChild(s)
								}
								if (h.controls) {
									var o = document.createElement("div");
									J(o, "".concat(b, "-cell__control")), J(o, "".concat(b,
										"-cell__control--prev")), z(o, E, k), n.appendChild(o)
								}
								if (J(r, "".concat(b, "-list")), J(i, "".concat(b, "-cell__body")),
									J(n, "".concat(b, "-cell")), J(n, "".concat(b, "-").concat(t,
										"s")), i.appendChild(r), n.appendChild(i), h.controls) {
									var c = document.createElement("div");
									J(c, "".concat(b, "-cell__control")), J(c, "".concat(b,
										"-cell__control--next")), z(c, E, y), n.appendChild(c)
								}
								u.appendChild(n), l.data[t] = a, l.render(t)
							}), n && (a.innerHTML = ""), a.appendChild(r), this.bind()
					}
				}
			}]) && r(e.prototype, t), i && r(e, i), n
		}();
	return W(de.prototype, ae, se, oe, ce), de.languages = o, de
});
