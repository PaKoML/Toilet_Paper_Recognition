import React from "react";
import styles from './index.css';
import imgA from './default_image.png';
require('./styles.css')


class Main extends React.Component{
    constructor(props) {
        super(props);
        this.state={
            files : []

        };
        this.onChange = this.onChange.bind(this);

    }
    onChange(e){
        var files = e.target.files;
        // slice : 얕은 복사 (원본 훼손 X)
        // call : 상위의 context 를 변경하는 메서드 ! 변경 !
        var filesArr = Array.prototype.slice.call(files);
        // ... : 전개연산자 : 정해지지 않은 갯수의 매개변수
        this.setState({files : [...this.state.files, ...filesArr]})
    }
    // != ,!== more strict
    removeFile(f) {
        this.setState({files:this.state.files.filter(x => x !== f)})

    }

    render() {
        return (
            <form>
                <div>
                    <label className="custom-file-upload">
                        <input type="file" multiple onChange={this.onChange} />
                        파일올리기
                    </label>
                    {
                        this.state.files.map(x=> <div className="file-preview" onClick = {this.removeFile.bind(this.x)}>{x.name}</div>)

                    }
                </div>
                <div className="wrap">
                    <a href="#" className="button">전송</a>
                </div>
                <img src={imgA} width="500px" height="500px" ></img>
                <img src={imgA} width="500px" height="500px" ></img>
            </form>

        )
    };

}

export default Main;