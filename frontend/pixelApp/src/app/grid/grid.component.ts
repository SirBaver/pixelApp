import { Component } from '@angular/core';

@Component({
  selector: 'app-grid',
  templateUrl: './grid.component.html',
  styleUrls: ['./grid.component.scss']
})
export class GridComponent {
  grid: any[] = [];

  constructor() {
    this.createGrid();
  }

  createGrid() {
    for (let i = 0; i < 100; i++) {
      this.grid[i] = [];
      for (let j = 0; j < 100; j++) {
        this.grid[i][j] = { color: '#ffffff' };
      }
    }
  }

  colorCell(cell: any) {
    cell.color = '#000000'; // Change this to the color you want
  }
}