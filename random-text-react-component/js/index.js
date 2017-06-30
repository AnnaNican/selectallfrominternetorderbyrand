'use strict';

var _class, _temp, _class2, _temp2;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var text = '\nSELECT * FROM INTERNET \nORDER BY RAND';

// Cycle animation
var fadeInOut = true;
// Time to complete animation. Proportional to framerate
var animationDuration = 1000;
// Time it takes each letter to fade in. Inversely proportional to framerate
var animationSpeed = 1000;
var fontSize = 50;

// Keep synced with scss
var numKeyframes = 20;

// Alternate Setup

// let text = `
// Wo ein treues Herze
// In Liebe vergeht,
// Da welken die Lilien
// Auf jedem Beet;
// Da muß in die Wolken
// Der Vollmond gehn,
// Damit seine Tränen
// Die Menschen nicht sehn;
// Da halten die Englein
// Die Augen sich zu
// Und schluchzen und singen
// Die Seele zur Ruh.`

// const fadeInOut = true;
// const animationDuration = 8000
// const animationSpeed = 800
// const fontSize = 34
// const numKeyframes = 20

// ---------------------------------------------------------------
text = text.replace(/\n/i, '');
var p = React.PropTypes;

var Letter = (_temp = _class = function (_React$Component) {
  _inherits(Letter, _React$Component);

  function Letter() {
    _classCallCheck(this, Letter);

    var _this = _possibleConstructorReturn(this, _React$Component.call(this));

    _this.state = {
      show: false,
      animate: true
    };
    _this.timeouts = [];
    return _this;
  }

  Letter.prototype.componentDidMount = function componentDidMount() {
    if (this.props.animate === 'in') {
      this._fadeIn();
    }
  };

  Letter.prototype.componentWillReceiveProps = function componentWillReceiveProps(nextProps) {
    if (nextProps.animate !== this.props.animate) {
      if (nextProps.animate === 'in') {
        this._fadeIn();
      } else {
        this._fadeOut();
      }
    }
  };

  Letter.prototype.shouldComponentUpdate = function shouldComponentUpdate(nextProps, nextState) {
    return nextState.fade !== this.state.fade || nextState.show !== this.state.show || nextProps.x !== this.props.x || nextProps.y !== this.props.y || nextProps.fontHeight !== this.props.fontHeight;
  };

  Letter.prototype.componentWillUnmount = function componentWillUnmount() {
    this.timeouts.forEach(function (timeout) {
      return clearTimeout(timeout);
    });
  };

  // render component and animate in

  Letter.prototype._fadeIn = function _fadeIn() {
    var _this2 = this;

    this.timeouts.push(setTimeout(function () {
      _this2.setState({
        fade: 'in',
        show: true
      });
      // Disable animation after fade in
      _this2.timeouts.push(setTimeout(function () {
        return _this2.setState({ animate: false });
      }, _this2.animationSpeed));
    }, this.props.animationStart + Math.random() * this.props.animationSpeed));
  };

  // animate out then stop rendering

  Letter.prototype._fadeOut = function _fadeOut() {
    var _this3 = this;

    this.timeouts.push(setTimeout(function () {
      _this3.setState({ fade: 'out', animate: true });
      _this3.timeouts.push(setTimeout(function () {
        _this3.setState({ show: false });
      }, _this3.props.animationSpeed));
    }, this.props.animationStart + Math.random() * this.props.animationSpeed));
  };

  Letter.prototype.render = function render() {
    if (!this.state.show) {
      return null;
    }
    var keyframe = Math.floor(Math.random() * this.props.numKeyframes + 1);
    var easingFunction = 'cubic-bezier(' + (Math.random() * .8 + +.1) + ',0,' + (Math.random() * .5 + .25) + ',1)';
    var proportionalPosition = this.props.i / this.props.textLen;
    var transitionDelay = proportionalPosition / 2 + Math.random() * proportionalPosition;
    return React.createElement(
      'div',
      {
        className: 'letter',
        style: {
          fontSize: this.props.fontHeight,
          height: this.props.fontHeight,
          width: this.props.fontHeight / 2,
          left: this.props.x,
          top: this.props.y,
          transition: '\n            top 1s ' + easingFunction + ' ' + transitionDelay + 's,\n            left 1s ' + easingFunction + ' ' + transitionDelay + 's,\n            font-size 1s ' + easingFunction + ' ' + transitionDelay + 's\n          ',
          animation: this.state.animate ? '\n              ' + ('fade-' + this.state.fade + '-' + keyframe) + '\n              ' + easingFunction + '\n              ' + this.props.animationSpeed + 'ms forwards\n            ' : null
        }
      },
      this.props.char
    );
  };

  return Letter;
}(React.Component), _class.propTypes = {
  x: p.number.isRequired,
  y: p.number.isRequired,
  i: p.number.isRequired,
  textLen: p.number.isRequired,
  char: p.string.isRequired,
  fontHeight: p.number.isRequired,
  numKeyframes: p.number.isRequired,
  animate: p.oneOf(['in', 'out']),
  animationSpeed: p.number.isRequired,
  animationStart: p.number.isRequired
}, _temp);
var RandomText = (_temp2 = _class2 = function (_React$Component2) {
  _inherits(RandomText, _React$Component2);

  function RandomText() {
    _classCallCheck(this, RandomText);

    var _this4 = _possibleConstructorReturn(this, _React$Component2.call(this));

    _this4.state = {
      numRows: null,
      chars: null,
      updated: false
    };
    return _this4;
  }

  RandomText.prototype.componentDidMount = function componentDidMount() {
    this.setState(this._mapCharPositions(this.props));
  };

  RandomText.prototype.componentWillReceiveProps = function componentWillReceiveProps(nextProps) {
    if (nextProps.fontHeight !== this.props.fontHeight || nextProps.width !== this.props.width) {
      this.setState(this._mapCharPositions(nextProps));
    }
  };

  RandomText.prototype.shouldComponentUpdate = function shouldComponentUpdate(nextProps, nextState) {
    if (this.state.updated) {
      this.setState({ updated: false });
      return true;
    }
    return nextProps.animate !== this.props.animate || this.state.chars === null;
  };

  // returns an array of chars w/ form [x, y, char]

  RandomText.prototype._mapCharPositions = function _mapCharPositions(props) {
    var fontWidth = props.fontHeight / 2;
    var charsPerRow = Math.floor(props.width / fontWidth);
    var emptySpaceInRow = props.width - charsPerRow * fontWidth;
    var margin = emptySpaceInRow / (charsPerRow + 1);
    var chars = [];
    var text = props.text.trim();
    var textLength = text.length;

    var firstLetterOfWord = true;
    for (var i = 0; i < textLength; i++) {
      var col = i % charsPerRow;

      // Don't push spaces into the array, and if there is a space at the
      // beginning of a line, remove it from the original text and put the next
      // character in its place
      if (text[i] === ' ') {
        firstLetterOfWord = true;
        if (col === 0) {
          text = text.slice(0, i) + text.slice(i + 1);
          i--;
          textLength--;
        }
      } else {
        // Handle text wrapping
        if (firstLetterOfWord) {
          var wordLength = 1;
          var wordCounter = 1;
          while (i + wordCounter < text.length && text[i + wordCounter] !== ' ') {
            wordLength++;
            wordCounter++;
          }
          firstLetterOfWord = false;

          var charsLeftInRow = charsPerRow - col;
          var indOfLastCharInRow = i + charsLeftInRow;
          // If the word is too long to fit on one line hyphenate it
          if (wordLength > charsPerRow) {
            text = text.slice(0, indOfLastCharInRow - 1) + '-' + text.slice(indOfLastCharInRow - 1);
            textLength++;
          }
          // Else insert spaces and adjust textLength to skip the word to the next line
          else if (wordLength > charsLeftInRow) {
              text = text.slice(0, i) + ' '.repeat(wordLength) + text.slice(i);
              textLength += wordLength;
            }
        }
        // Push the char at i into the return arr
        chars.push([col * fontWidth + margin * (col + 1), // x
        Math.floor(i / charsPerRow) * props.fontHeight, // y
        text[i]]);
      }
    }
    var numRows = Math.ceil(textLength / charsPerRow);
    return { numRows: numRows, chars: chars, updated: true };
  };

  RandomText.prototype.render = function render() {
    var _this5 = this;

    if (this.state.chars == null) {
      return null;
    } else {
      return React.createElement(
        'div',
        {
          className: 'container' + ' ' + this.props.className,
          style: {
            height: this.state.numRows * this.props.fontHeight,
            width: this.props.width
          } },
        this.state.chars.map(function (char, i) {
          return React.createElement(Letter, {
            x: char[0],
            y: char[1],
            char: char[2],
            fontHeight: _this5.props.fontHeight,
            numKeyframes: numKeyframes,
            key: i,
            i: i,
            textLen: _this5.props.text.length,
            animate: _this5.props.animate,
            animationSpeed: _this5.props.animationSpeed,
            animationStart: (_this5.props.animationDuration - _this5.props.animationSpeed) / _this5.state.chars.length * i
          });
        })
      );
    }
  };

  return RandomText;
}(React.Component), _class2.propTypes = {
  text: p.string.isRequired,
  className: p.string,
  width: p.number.isRequired,
  // Sets font-size
  fontHeight: p.number.isRequired,
  // Duration of each letter's fade in animation
  animationSpeed: p.number.isRequired,
  // Total animation duration (not counting randomness factor)
  animationDuration: p.number.isRequired,
  animate: p.oneOf(['in', 'out']),
  homePage: p.bool
}, _temp2);

var App = function (_React$Component3) {
  _inherits(App, _React$Component3);

  function App() {
    _classCallCheck(this, App);

    var _this6 = _possibleConstructorReturn(this, _React$Component3.call(this));

    _this6.state = {
      animate: 'in',
      width: document.body.offsetWidth * .6
    };
    if (fadeInOut) {
      setInterval(function () {
        _this6.setState({ animate: _this6.state.animate == 'in' ? 'out' : 'in' });
      }, animationDuration + 5000);
    }
    return _this6;
  }

  App.prototype.componentWillMount = function componentWillMount() {
    this._setupResizeListener();
  };

  App.prototype.render = function render() {
    return React.createElement(RandomText, {
      width: this.state.width,
      text: text,
      fontHeight: fontSize,
      animate: this.state.animate,
      animationDuration: animationDuration,
      animationSpeed: animationSpeed });
  };

  App.prototype._getWindowWidth = function _getWindowWidth() {
    return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
  };

  App.prototype._setupResizeListener = function _setupResizeListener() {
    // Create "window.throttledResize" event that listens to resize and throttles it to fire once per frame at most
    // https://developer.mozilla.org/en-US/docs/Web/Events/resize#requestAnimationFrame_customEvent
    var running = false;
    var throttleResize = function throttleResize() {
      if (!running) {
        running = true;
        requestAnimationFrame(function () {
          window.dispatchEvent(new CustomEvent('throttledResize'));
          running = false;
        });
      }
    };
    window.addEventListener('resize', throttleResize);
    window.addEventListener('throttledResize', this._handleResize.bind(this));
  };

  App.prototype._handleResize = function _handleResize() {
    var width = this._getWindowWidth();
    if (Math.abs(width * .6 - this.state.width) > 100) {
      this.setState({ width: width * .6 });
    }
  };

  return App;
}(React.Component);

ReactDOM.render(React.createElement(App, null), document.getElementById('app'));