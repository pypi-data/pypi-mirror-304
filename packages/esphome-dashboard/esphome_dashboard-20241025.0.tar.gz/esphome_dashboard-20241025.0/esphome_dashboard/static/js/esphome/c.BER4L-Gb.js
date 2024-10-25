import{H as o,b as t,c as s,n as i,s as e,x as n,J as a,h as l}from"./index-DxTkLEpY.js";import"./c.CG9mkB5F.js";import"./c.CrXQjN4Z.js";let c=class extends e{render(){return n`
      <esphome-process-dialog
        .heading=${`Clean ${this.configuration}`}
        .type=${"clean"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_openInstall(){l(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=[o],t([s()],c.prototype,"configuration",void 0),c=t([i("esphome-clean-dialog")],c);
//# sourceMappingURL=c.BER4L-Gb.js.map
