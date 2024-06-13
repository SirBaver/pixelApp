import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RegisterWaitingPage } from './register-waiting.page';

describe('RegisterWaitingPage', () => {
  let component: RegisterWaitingPage;
  let fixture: ComponentFixture<RegisterWaitingPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterWaitingPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
