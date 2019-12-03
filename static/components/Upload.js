import React from "react";
import "../style/frameworks.css";
import "../style/softx.css";

const valid_image_types = ["image/png", "image/tiff", "image/jpeg", "image/gif"];

class Upload extends React.Component{

    constructor(props){
        super(props);

        this.state = { 
            termsConditionChecked: false,
            hightlight: false,
            uploadedFiles : []
        };

        this.onFilesAdded = this.onFilesAdded.bind(this);
        this.onDragOver = this.onDragOver.bind(this);
        this.onDragLeave = this.onDragLeave.bind(this);
        this.onDrop = this.onDrop.bind(this);

        this.processFiles = this.processFiles.bind(this);
    }

    openFileUpload = (e) => {
        this.inputElement.click();
    }

    onFilesAdded(e) {
        this.processFiles(Object.values(e.target.files));
    }

    onDragOver(e) {
        e.preventDefault();      
        this.setState({ hightlight: true });
    }

    onDragLeave() {
        this.setState({ hightlight: false });
    }
    
    onDrop(e) {
        e.preventDefault();
        this.processFiles(Object.values(e.dataTransfer.files));
        this.setState({ hightlight: false });
    }


    processFiles(uFiles){
        var filteredFiles = [];
        
        for (var i=0, len = uFiles.length; i < len; i++){
            if (valid_image_types.includes(uFiles[i].type)){
                filteredFiles.push(uFiles[i]);
            }
        }
        this.setState({
            uploadedFiles : this.state.uploadedFiles.concat(filteredFiles)
        });
    }


    checkTermsConditions = e => {
        this.setState({
            termsConditionChecked: !this.state.termsConditionChecked
        });
    };

    upload = () => {
        if (this.state.uploadedFiles.length){
            if (this.state.termsConditionChecked){
                this.props.onFilesAdded(this.state.uploadedFiles);
            }else{
                alert("Please accept the Terms & Conditions and Pivacy & Policy.")
            }
        }else{
            alert("Please upload one or more scans.")
        }
        
    };

    defaultClick = (e) =>{
        e.preventDefault();
    }



    render(){
        if (!this.props.show) {
            return null;
        }
        
        return (   
                    
            <div className="modal-content">
                <span className="close" onClick={this.props.onClose} >&times;</span>
                <h2>Upload For Analysis</h2>
                <p>JPG / PNG (Preffered Ratio 5:8)</p>
                <div className={`drop ${this.state.hightlight ? "Highlight" : ""}`} 
                    onClick={this.openFileUpload}
                    onDragOver={this.onDragOver}
                    onDragLeave={this.onDragLeave}
                    onDrop={this.onDrop}>
                        <img src={require("../assets/icons/upload.png")} alt="" /> 
                        <br />
                        Click to Search or Drag &amp; Drop Your X-Ray Files Here
                </div>
                <div className="list"> 
                    {this.state.uploadedFiles.map((file,i) => (
                        <b key={i}>Selected File: {file.name}</b>
                    ))}
                </div>

                {/* For select directories webkitdirectory="true" */}
                <input type="file" multiple 
                    ref={input => this.inputElement = input} 
                    style={{display : 'none'}} 
                    className="uploaderx"
                    onChange={this.onFilesAdded} />

                <div className="status">
                    {   this.state.uploadedFiles.length > 0 &&
                        <h4>
                            The files are ready to be uploaded upon submission.
                        </h4>
                    }
                </div>
                <b><input type="checkbox"  check="false" onChange={this.checkTermsConditions} /> I agree to the <a href="/#" onClick={this.defaultClick}>Terms &amp; Conditions</a>  and  <a href="/#" onClick={this.defaultClick}> Privacy &amp; Policy</a> </b> 
                <button onClick={this.upload }> Upload X-Ray Scans To Server</button>
            </div>
                    

        );
    }
    
}

export default Upload;
